# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import os
import platform
import tempfile
from xml.etree import ElementTree

from PyQt4.QtGui import QMainWindow, QApplication, QImage, QPixmap, QSystemTrayIcon, QIcon
from PyQt4.QtCore import pyqtSignature, pyqtSignal, Qt, QString, QDate, QTimer, QProcess, QUrl, QObject, QSize
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from Ui_mainwindow import Ui_MainWindow
from ui.custom_widgets import SystemTrayIcon, ListWidgetItem
from ui.settings import Settings


class ImageDownloader(QObject):

    # Signals.
    download_finished = pyqtSignal(QImage, QDate, str)
    thumbnail_download_finished = pyqtSignal(QImage, str, str)
    status_text = pyqtSignal(QString)

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.resolution = '1920x1200'
        self.last_image_url = None
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.reply_finished)

    def set_resolution(self, resolution):
        """
        Set the image resolution.
        :param resolution: 1024x768, 1280x720, 1366x768, 1920x1200
        """
        self.resolution = resolution

    def _get_url(self, url_string, request_type=None, request_metadata=None):
        url = QUrl(url_string)
        request = QNetworkRequest(QUrl(url))
        if not request_type is None:
            request.setAttribute(QNetworkRequest.User, (request_type, request_metadata))
        self.manager.get(request)

    def get_daily_wallpaper(self):
        self.status_text.emit('Checking for wallpaper update...')
        xml_url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-ww'
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
            if image_url == self.last_image_url:
                print 'Image is the same as last downloaded image.'
                self.download_finished.emit(QImage(), QDate(), '')
                return
            self.status_text.emit('Downloading image...')
            self.last_image_url = image_url
            self._get_url(image_url, 1, (start_date, copyright_info))
        else:
            for image_number in xrange(len(root) - 1):
                url = 'http://www.bing.com' + root[image_number].find('url').text
                date_string = str(QDate.fromString(root[image_number].find('startdate').text,
                                                   'yyyyMMdd').toString('dddd dd MMMM'))
                copyright_info = root[image_number].find('copyright').text
                self._get_url(url, 4, (date_string, copyright_info))

    def reply_finished(self, reply):
        url = reply.url()
        print 'URL Downloaded:', str(url.toEncoded())
        if reply.error():
            error_message = str(reply.errorString())
            print 'Download of %s failed: %s' % (url.toEncoded(), error_message)
        else:
            # print 'Mime-type:', str(reply.header(QNetworkRequest.ContentTypeHeader).toString())
            data = reply.readAll()
            attribute = reply.request().attribute(QNetworkRequest.User)
            if not attribute.isNull():
                request_type, request_metadata = attribute.toPyObject()
                if request_type == 0:
                    # Daily wallpaper XML.
                    self.parse_daily_xml(data, True)
                elif request_type == 1:
                    start_date, copyright_info = request_metadata
                    wallpaper_image = QImage.fromData(data)
                    self.download_finished.emit(wallpaper_image, start_date, copyright_info)
                if request_type == 3:
                    # Daily wallpaper XML.
                    day_index = request_metadata
                    self.parse_daily_xml(data, False, day_index)
                elif request_type == 4:
                    label, copyright_info = request_metadata
                    wallpaper_image = QImage.fromData(data)
                    self.thumbnail_download_finished.emit(wallpaper_image, label, copyright_info)


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.app = QApplication.instance()

        # Set window title to include application version number.
        title = '%s - v%s' % (str(self.app.applicationName()), str(self.app.applicationVersion()))
        self.setWindowTitle(title)
        self.lbl_version.setText(QString('Version %1').arg(self.app.applicationVersion()))

        self.preview_image = QImage()
        self.refresh_timer = QTimer()
        self.lbl_status.setText('')
        self.settings = Settings()
        self.load_settings()

        self.system_tray_icon = SystemTrayIcon(self.app.windowIcon(), self)
        self.system_tray_icon.activated.connect(self.system_tray_icon_activated)
        self.system_tray_icon.show()

        self.image_downloader = ImageDownloader()
        self.image_downloader.status_text.connect(self.update_status_text)
        self.image_downloader.download_finished.connect(self.download_finished)
        self.image_downloader.thumbnail_download_finished.connect(self.thumbnail_download_finished)
        self.on_button_refresh_released()

        self.refresh_timer.timeout.connect(self.on_button_refresh_released)
        if self.cb_auto_update.isChecked():
            self.refresh_timer.start()

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.update_preview_size()

    def closeEvent(self, event):
        if self.sender() is self.system_tray_icon.exit_action:
            QMainWindow.closeEvent(self, event)
        else:
            event.ignore()
            self.setVisible(False)

    def update_status_text(self, text):
        self.lbl_status.setText(text)
        self.app.processEvents()

    def load_settings(self):
        self.cb_resolution.setCurrentIndex(self.settings.get_image_resolution())

        self.sb_update_interval.setValue(self.settings.get_auto_update_interval() / 60000)
        self.on_sb_update_interval_valueChanged(self.sb_update_interval.value())
        self.cb_auto_update.setChecked(self.settings.get_auto_update_enabled())

        self.cb_run_command.setChecked(self.settings.get_run_command_enabled())
        self.le_command.setText(self.settings.get_run_command_command())

    def system_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()
            self.raise_()
            self.update_preview_size()

    def download_finished(self, wallpaper_image, start_date, copyright_info):
        if not wallpaper_image.isNull():
            self.preview_image = wallpaper_image
            self.update_preview_size()
            self.lbl_image_info.setText(copyright_info)
            self.lbl_image_date.setText(start_date.toString('dddd, dd MMMM yyyy'))
            self.system_tray_icon.setToolTip(QString('%1\n%2').arg(self.app.applicationName(), copyright_info))
            self.app.processEvents()
            self.apply_wallpaper()
        self.button_refresh.setEnabled(True)
        self.lbl_status.setText('')

    def thumbnail_download_finished(self, thumbnail_image, label, copyright_info):
        icon = QIcon(QPixmap.fromImage(thumbnail_image.scaled(QSize(200, 200), Qt.KeepAspectRatio)))
        widget_item = ListWidgetItem(icon, label)
        widget_item.setToolTip(copyright_info)
        self.lw_wallpaper_history.addItem(widget_item)
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
        print 'Applying wallpaper...'
        self.update_status_text('Applying wallpaper...')
        temp_path = os.path.join(tempfile.gettempdir(), 'bing_wallpaper.jpg')
        self.preview_image.save(temp_path, quality=100)

        system_platform = platform.system()
        if system_platform == 'Windows':
            import ctypes
            SPI_SETDESKWALLPAPER = 20  # According to http://support.microsoft.com/default.aspx?scid=97142
            ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, temp_path, 1)
        elif system_platform == 'Linux':
            file_url = QUrl.fromLocalFile(temp_path)
            file_string = unicode(file_url.toString())
            error = QProcess.execute('gsettings set org.gnome.desktop.background picture-uri ' + file_string)
            if error:
                self.system_tray_icon.showMessage('Error applying wallpaper',
                                                  'The wallpaper could not be set.',
                                                  QSystemTrayIcon.Critical)

        if self.cb_run_command.isChecked() and self.le_command.text():
            self.update_status_text('Running custom command...')
            error = QProcess.execute(self.le_command.text())
            if error:
                self.system_tray_icon.showMessage('Error running command',
                                                  'The command specified in the settings failed to run. Please check '
                                                  'the path.',
                                                  QSystemTrayIcon.Critical)

    @pyqtSignature('int')
    def on_cb_resolution_currentIndexChanged(self, index):
        self.settings.set_image_resolution(index)
        self.image_downloader.set_resolution(str(self.cb_resolution.currentText()))

    @pyqtSignature('bool')
    def on_cb_auto_update_toggled(self, enabled):
        self.settings.set_auto_update_enabled(enabled)
        if enabled:
            self.refresh_timer.start()
        else:
            self.refresh_timer.stop()

    @pyqtSignature('int')
    def on_sb_update_interval_valueChanged(self, minutes):
        print 'INTERVAL CHANGED:', minutes
        if minutes == 1:
            self.sb_update_interval.setSuffix(' minute')
        else:
            self.sb_update_interval.setSuffix(' minutes')
        interval = minutes * 60000
        self.settings.set_auto_update_interval(interval)
        self.refresh_timer.stop()
        self.refresh_timer.setInterval(interval)
        if self.cb_auto_update.isChecked():
            self.refresh_timer.start()

    @pyqtSignature('bool')
    def on_cb_run_command_toggled(self, enabled):
        self.settings.set_run_command_enabled(enabled)

    @pyqtSignature('QString')
    def on_le_command_textEdited(self, text):
        self.settings.set_run_command_command(text)

    @pyqtSignature('')
    def on_button_close_released(self):
        """
        Slot documentation goes here.
        """
        self.close()

    @pyqtSignature('')
    def on_button_refresh_released(self):
        """
        Slot documentation goes here.
        """
        print 'Refreshing...'
        self.image_downloader.set_resolution(str(self.cb_resolution.currentText()))
        self.button_refresh.setEnabled(False)
        self.image_downloader.get_daily_wallpaper()

    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, index):
        if index == 2:
            print 'History'
            self.lw_wallpaper_history.clear()
            self.lw_wallpaper_history.setIconSize(QSize(200, 200))
            for day_index in [0, 8]:
                self.image_downloader.get_history_thumbs(day_index)

