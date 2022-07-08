# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
import platform
import tempfile
from xml.etree import ElementTree
import re

import shutil
from PyQt5.QtGui import QImage, QPixmap, QIcon, QImageReader
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QFileDialog, QListWidgetItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QDate, QTimer, QProcess, QUrl, QObject, QSize
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

from ui.custom_widgets import SystemTrayIcon
from .Ui_mainwindow import Ui_MainWindow
from ui.databases import CopyrightDatabase
from ui.message_boxes import message_box_error
from ui.settings import Settings
from ui.wallpaper_changer import WallpaperChanger


re_archive_file = re.compile(r'[0-9]{8}\.jpg')


class ImageDownloader(QObject):

    TYPE_META = 1000
    ATTEMPTS = 1001

    # Signals.
    download_finished = pyqtSignal(QImage, QDate, str)
    download_failed = pyqtSignal(str)
    thumbnail_download_finished = pyqtSignal(QImage, QDate, str, int)
    status_text = pyqtSignal(str)

    def __init__(self, parent=None):
        super(ImageDownloader, self).__init__(parent)
        self.resolution = '1920x1200'
        self.last_image_url = None
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.reply_finished)

    def set_resolution(self, resolution):
        """
        Set the image resolution.

        @param resolution: 1024x768, 1280x720, 1366x768, 1920x1200
        @type: str
        """
        self.resolution = resolution

    def _get_url(self, url_string, request_type=None, request_metadata=None):
        url = QUrl(url_string)
        request = QNetworkRequest(QUrl(url))
        if request_type is not None:
            request.setAttribute(self.TYPE_META, (request_type, request_metadata))
        self.manager.get(request)

    def get_full_wallpaper(self, day_index=0):
        self.status_text.emit('Checking for wallpaper update...')
        xml_url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx={}&n=1&mkt=en-ww'.format(day_index)
        self._get_url(xml_url, 0)

    def get_history_thumbs(self, day_index=0):
        xml_url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx={}&n=8&mkt=en-ww'.format(day_index)
        self._get_url(xml_url, 3, day_index)

    def parse_daily_xml(self, xml_data, full_image=False, day_index=0):
        root = ElementTree.fromstring(xml_data)

        if full_image:
            base_url = 'http://www.bing.com' + root[0].find('urlBase').text
            start_date = QDate.fromString(root[0].find('startdate').text, 'yyyyMMdd')
            copyright_info = root[0].find('copyright').text

            image_url = '{}_{}.jpg'.format(base_url, self.resolution)
            print(image_url)
            if image_url == self.last_image_url:
                print(f'Image is the same as last downloaded image. ({image_url})')
                self.download_finished.emit(QImage(), QDate(), '')
                return
            self.status_text.emit('Downloading image...')
            self.last_image_url = image_url
            self._get_url(image_url, 1, (start_date, copyright_info))
        else:
            for image_number in range(len(root) - 1):
                image_day_index = image_number + day_index
                url = 'http://www.bing.com' + root[image_number].find('url').text
                image_date = QDate.fromString(root[image_number].find('startdate').text, 'yyyyMMdd')
                copyright_info = root[image_number].find('copyright').text
                self._get_url(url, 4, (image_date, copyright_info, image_day_index))

    def reply_finished(self, reply):
        url = reply.url()
        request = reply.request()
        print('URL Downloaded:', str(url.toEncoded()))
        if reply.error():
            attempts = request.attribute(self.ATTEMPTS)
            attempts = 0 if attempts is None else attempts
            if attempts <= 10:
                request.setAttribute(self.ATTEMPTS, attempts + 1)
                print('Network not available. Trying again in 5 seconds...', self.manager.networkAccessible())
                QTimer.singleShot(5000, lambda: self.manager.get(request))
                return

            error_message = str(reply.errorString())
            self.download_failed.emit(error_message)
            print('Download of {0:s} failed: {1:s}'.format(url.toEncoded(), error_message))
        else:
            # print 'Mime-type:', str(reply.header(QNetworkRequest.ContentTypeHeader).toString())
            data = reply.readAll()
            attribute = request.attribute(self.TYPE_META)

            try:
                request_type, request_metadata = attribute
            except (IndexError, TypeError):
                return

            if request_type == 0:  # Daily wallpaper XML.
                self.parse_daily_xml(data, True)
            elif request_type == 1:
                start_date, copyright_info = request_metadata
                wallpaper_image = QImage.fromData(data)
                self.download_finished.emit(wallpaper_image, start_date, copyright_info)
            if request_type == 3:  # History thumbnails.
                day_index = request_metadata
                self.parse_daily_xml(data, False, day_index)
            elif request_type == 4:
                image_date, copyright_info, image_day_index = request_metadata
                wallpaper_image = QImage.fromData(data)
                self.thumbnail_download_finished.emit(wallpaper_image, image_date, copyright_info, image_day_index)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.app = QApplication.instance()

        # Set window title to include application version number.
        title = '{0:s} - v{1:s}'.format(
            self.app.applicationName(),
            self.app.applicationVersion()
        )
        self.setWindowTitle(title)
        self.lbl_version.setText('Version {0:s}'.format(self.app.applicationVersion()))
        self.system_tray_icon = SystemTrayIcon(self.app.windowIcon(), self)

        if platform.system() != 'Linux':
            self.tabWidget.removeTab(2)

        self.preview_image = QImage()
        self.refresh_timer = QTimer()
        self.lbl_status.setText('')
        self.settings = Settings()
        self.load_settings()

        self.cb_change_method.currentIndexChanged.connect(self.change_method_changed)

        self.changer = WallpaperChanger()
        self.copyright_db = CopyrightDatabase()

        self.system_tray_icon.activated.connect(self.system_tray_icon_activated)
        self.system_tray_icon.show()

        self.image_downloader = ImageDownloader()
        self.image_downloader.status_text.connect(self.update_status_text)
        self.image_downloader.download_failed.connect(self.download_failed)
        self.image_downloader.download_finished.connect(self.download_finished)
        self.image_downloader.thumbnail_download_finished.connect(self.thumbnail_download_finished)
        self.on_button_refresh_released()

        self.queued_refresh = False
        self.refresh_timer.timeout.connect(self.on_button_refresh_released)
        if self.cb_auto_update.isChecked():
            self.refresh_timer.start()

    def resizeEvent(self, event):
        """
        @type event: QEvent
        """
        super(MainWindow, self).resizeEvent(event)
        self.update_preview_size()

    def closeEvent(self, event):
        """
        @type event: QEvent
        """
        if self.sender() is self.system_tray_icon.exit_action:
            super(MainWindow, self).closeEvent(event)
        else:
            event.ignore()
            self.setVisible(False)

    def update_system_tray_icon(self, icon_colour=None):
        if icon_colour is None:
            icon_colour = self.settings.icon_colour

        if icon_colour == 1:
            white_icon = QIcon(':/icons/ui/ot_icon_white.svg')
            self.system_tray_icon.setIcon(white_icon)
        else:
            self.system_tray_icon.setIcon(self.app.windowIcon())

    def update_status_text(self, text):
        """
        @type text: str
        """
        self.lbl_status.setText(text)
        self.app.processEvents()

    def load_settings(self):
        self.cb_resolution.setCurrentIndex(self.settings.image_resolution)

        self.sb_update_interval.setValue(self.settings.auto_update_interval // 60000)
        self.on_sb_update_interval_valueChanged(self.sb_update_interval.value())
        self.cb_auto_update.setChecked(self.settings.auto_update_enabled)

        self.cb_run_command.setChecked(self.settings.run_command_enabled)
        self.le_command.setText(self.settings.run_command_command)

        self.cb_enable_archive.setChecked(self.settings.archive_enabled)
        self.le_archive_location.setText(self.settings.archive_location)

        if self.settings.icon_colour == 0:
            self.rb_icon_colour_black.setChecked(True)
        else:
            self.rb_icon_colour_white.setChecked(True)

        # Set desktop environment.
        env_name = self.settings.linux_desktop
        env_index = self.cb_change_method.findText(env_name, Qt.MatchFixedString)
        self.cb_change_method.setCurrentIndex(env_index)

    def system_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.update_preview_size()

    def download_failed(self, error_message):
        """
        Report that the download failed to the user and re-enable the Refresh button
        :type error_message: QString
        :return:
        :rtype:
        """
        self.lbl_status.setText(error_message)
        self.button_refresh.setEnabled(True)

        self.lbl_image_preview.setPixmap(QPixmap())
        self.lbl_image_preview.setText('[NO PREVIEW]')
        self.lbl_image_info.setText('Last download attempt failed.')

    def download_finished(self, wallpaper_image, start_date, copyright_info):
        """
        @type wallpaper_image: QImage
        @type start_date: QDate
        @type copyright_info: str
        """
        if not wallpaper_image.isNull():
            self.preview_image = wallpaper_image
            self.update_preview_size()
            self.lbl_image_info.setText(copyright_info)
            self.lbl_image_date.setText(start_date.toString('dddd, dd MMMM yyyy'))
            self.system_tray_icon.setToolTip('{0:s}\n{1:s}'.format(self.app.applicationName(), copyright_info))
            self.app.processEvents()
            self.apply_wallpaper()
            self.copyright_db.set_info(start_date, copyright_info)
            if self.settings.archive_enabled:
                self.save_wallpaper(wallpaper_image, start_date)
        self.button_refresh.setEnabled(True)
        self.lbl_status.setText('')

    def thumbnail_download_finished(self, thumbnail_image, image_date, copyright_info, image_day_index):
        """
        @type thumbnail_image: QImage
        @type label: str
        @type copyright_info: str
        @type image_day_index: int
        """
        archive_path = self.get_archive_path(image_date)
        if not os.path.isfile(archive_path):
            archive_path = None
        self.lw_wallpaper_history.add_item(thumbnail_image, image_date, copyright_info, image_day_index, archive_path)
        self.lw_wallpaper_history.sortItems(Qt.AscendingOrder)

    def update_preview_size(self):
        if self.preview_image.isNull():
            return
        label_size = self.lbl_image_preview.size()
        resized_pixmap = QPixmap.fromImage(self.preview_image).scaled(label_size,
                                                                      Qt.KeepAspectRatio,
                                                                      Qt.SmoothTransformation)
        self.lbl_image_preview.setPixmap(resized_pixmap)

    def apply_wallpaper(self):
        """
        Slot documentation goes here.
        """
        print('Applying wallpaper...')
        self.update_status_text('Applying wallpaper...')
        temp_path = os.path.join(tempfile.gettempdir(), 'bing_wallpaper.jpg')
        self.preview_image.save(temp_path, quality=100)
        self.changer.apply_wallpaper(temp_path)

        if self.cb_run_command.isChecked() and self.le_command.text():
            self.update_status_text('Running custom command...')
            error = QProcess.execute(self.le_command.text())
            if error:
                self.system_tray_icon.showMessage('Error running command',
                                                  'The command specified in the settings failed to run. Please check '
                                                  'the path.',
                                                  QSystemTrayIcon.Critical)

        # Check for --quit command switch to see if we need to quit now that the wallpaper has been applied.
        if self.app.args.quit:
            print('Closing application...')
            self.app.quit()

    def get_archive_path(self, image_date):
        output_filename = '{0:s}.jpg'.format(image_date.toString('yyyyMMdd'))
        output_path = os.path.join(str(self.settings.archive_location), output_filename)
        return output_path

    def save_wallpaper(self, image, image_date):
        """
        Save image to archive folder.

        :type image: QImage
        :type image_date: QDate
        """
        output_path = self.get_archive_path(image_date)
        image.save(output_path)

    def get_archive_wallpapers(self):
        """
        Generator returning the date, path and copyright info (via db lookup) of each file found in the
        archive location.

        :rtype: QDate, unicode, unicode
        """
        image_reader = QImageReader()
        regex_date_split = re.compile(r'(\d{4})(\d{2})(\d{2})')

        copyright_info = self.copyright_db.get_all_info()
        archive_folder = self.settings.archive_location
        for filename in reversed([x for x in os.listdir(archive_folder) if re_archive_file.match(x)]):
            year, month, day = list(map(int, regex_date_split.findall(filename)[0]))
            wallpaper_date = QDate(year, month, day)
            wallpaper_copyright = copyright_info.get('{0:04d}-{1:02d}-{2:02d}'.format(year, month, day), '')
            wallpaper_filename = os.path.join(str(archive_folder), filename)

            image_reader.setFileName(wallpaper_filename)
            image_size = image_reader.size()
            image_size.scale(QSize(200, 125), Qt.IgnoreAspectRatio)
            image_reader.setScaledSize(image_size)
            thumbnail_image = image_reader.read()
            if thumbnail_image.isNull():
                continue
            self.lw_wallpaper_history.add_item(thumbnail_image, wallpaper_date, wallpaper_copyright,
                                               archive_path=wallpaper_filename)
            self.app.processEvents()
        self.lw_wallpaper_history.sortItems(Qt.AscendingOrder)

    def change_method_changed(self, index):
        self.settings.linux_desktop = index

    @pyqtSlot(int)
    def on_cb_resolution_currentIndexChanged(self, index):
        self.settings.image_resolution = index
        self.image_downloader.set_resolution(str(self.cb_resolution.currentText()))

    @pyqtSlot(bool)
    def on_cb_auto_update_toggled(self, enabled):
        self.settings.auto_update_enabled = enabled
        if enabled:
            self.refresh_timer.start()
        else:
            self.refresh_timer.stop()

    @pyqtSlot(int)
    def on_sb_update_interval_valueChanged(self, minutes):
        print('INTERVAL CHANGED:', minutes)
        if minutes == 1:
            self.sb_update_interval.setSuffix(' minute')
        else:
            self.sb_update_interval.setSuffix(' minutes')
        interval = minutes * 60000
        self.settings.auto_update_interval = interval
        self.refresh_timer.stop()
        self.refresh_timer.setInterval(interval)
        if self.cb_auto_update.isChecked():
            self.refresh_timer.start()

    @pyqtSlot(bool)
    def on_cb_run_command_toggled(self, enabled):
        self.settings.run_command_enabled = enabled

    @pyqtSlot(str)
    def on_le_command_textEdited(self, text):
        self.settings.run_command_command = text

    @pyqtSlot(bool)
    def on_cb_enable_archive_toggled(self, enabled):
        self.settings.archive_enabled = enabled

    @pyqtSlot()
    def on_button_archive_browse_released(self):
        path = QFileDialog.getExistingDirectory(None, 'Select archive location')
        if not path or not os.path.isdir(path):
            return

        self.le_archive_location.setText(path)
        self.on_le_archive_location_textEdited(path)

    @pyqtSlot(str)
    def on_le_archive_location_textEdited(self, text):
        if not text or not os.path.isdir(text):
            return
        self.settings.archive_location = text

    @pyqtSlot(bool)
    def on_rb_icon_colour_black_toggled(self, enabled):
        if enabled:
            self.settings.icon_colour = 0
            self.update_system_tray_icon(0)

    @pyqtSlot(bool)
    def on_rb_icon_colour_white_toggled(self, enabled):
        if enabled:
            self.settings.icon_colour = 1
            self.update_system_tray_icon(1)

    @pyqtSlot()
    def on_button_close_released(self):
        """
        Slot documentation goes here.
        """
        self.close()

    @pyqtSlot()
    def on_button_refresh_released(self):
        """
        Slot documentation goes here.
        """
        print('Refreshing...')
        self.image_downloader.set_resolution(str(self.cb_resolution.currentText()))
        self.button_refresh.setEnabled(False)
        self.image_downloader.get_full_wallpaper()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, index):
        self.lw_wallpaper_history.clear()
        history_index = self.tabWidget.indexOf(self.tab_history)
        if index == history_index:
            print('History')
            self.lw_wallpaper_history.setIconSize(QSize(200, 200))
            for day_index in [0, 8, 16]:
                self.image_downloader.get_history_thumbs(day_index)
            if self.settings.archive_enabled:
                self.get_archive_wallpapers()

    @pyqtSlot(QListWidgetItem)
    def on_lw_wallpaper_history_itemDoubleClicked(self, item):
        day_index = item.image_day_index
        print('Item with index {0:d} clicked!'.format(day_index))
        if day_index == -1:
            # Item is a wallpaper from the archive folder.
            try:
                archive_path = item.archive_path
            except AttributeError:
                return
            print('Applying wallpaper from', archive_path)
            temp_path = os.path.join(tempfile.gettempdir(), 'bing_wallpaper.jpg')
            try:
                shutil.copyfile(archive_path, temp_path)
            except IOError:
                message_box_error('Error applying wallpaper', 'Could not copy wallpaper image to temp folder.')
                return
            self.update_status_text('Applying wallpaper...')
            self.changer.apply_wallpaper(temp_path)
            self.update_status_text('')
        else:
            # The day index is still available. Start the download.
            self.image_downloader.get_full_wallpaper(item.image_day_index)

