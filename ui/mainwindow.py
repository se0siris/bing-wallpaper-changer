# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""
import ctypes
import os
import tempfile
import urllib2
from xml.etree import ElementTree

from PyQt4.QtGui import QMainWindow, QApplication, QImage, QPixmap, QSystemTrayIcon
from PyQt4.QtCore import pyqtSignature, QThread, pyqtSignal, Qt, QString, QDate, QTimer

from Ui_mainwindow import Ui_MainWindow
from ui.custom_widgets import SystemTrayIcon


class ImageDownloader(QThread):

    # Signals.
    download_finished = pyqtSignal(QImage, QDate, str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.resolution = '1920x1200'
        self.last_image_url = None

    def set_resolution(self, resolution):
        """
        Set the image resolution.
        :param resolution: 1024x768, 1280x720, 1366x768, 1920x1200
        """
        self.resolution = resolution

    def run(self):
        """
        Download the latest image and return it with date and copyright info.
        """
        xml_url = 'http://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=en-ww'
        page = urllib2.urlopen(xml_url)
        xml_content = page.read()
        page.close()
        root = ElementTree.fromstring(xml_content)
        base_url = 'http://www.bing.com' + root[0].find('urlBase').text
        start_date = QDate.fromString(root[0].find('startdate').text, 'yyyyMMdd')
        copyright_info = root[0].find('copyright').text

        image_url = '{}_{}.jpg'.format(base_url, self.resolution)
        if image_url == self.last_image_url:
            print 'Image is the same as last downloaded image.'
            self.download_finished.emit(QImage(), QDate(), '')
            return
        self.last_image_url = image_url
        print image_url

        image_data = urllib2.urlopen(image_url)
        wallpaper_image = QImage.fromData(image_data.read())
        image_data.close()
        print 'Image downloaded'
        self.download_finished.emit(wallpaper_image, start_date, copyright_info)


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

        self.preview_pixmap = QPixmap()

        self.system_tray_icon = SystemTrayIcon(self.app.windowIcon(), self)
        self.system_tray_icon.activated.connect(self.system_tray_icon_activated)
        self.system_tray_icon.show()

        self.image_downloader = ImageDownloader()
        self.image_downloader.download_finished.connect(self.download_finished)
        self.on_button_refresh_released()

        self.refresh_timer = QTimer()
        self.refresh_timer.setInterval(1200000)   # 20 minutes.
        self.refresh_timer.timeout.connect(self.on_button_refresh_released)
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

    def system_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.setVisible(True)
            self.setFocus()
            self.update_preview_size()

    def download_finished(self, wallpaper_image, start_date, copyright_info):
        if not wallpaper_image.isNull():
            self.preview_pixmap = QPixmap.fromImage(wallpaper_image)
            self.update_preview_size()
            self.lbl_image_info.setText(copyright_info)
            self.lbl_image_date.setText(start_date.toString('dddd, dd MMMM, yyyy'))
            self.system_tray_icon.setToolTip(QString('%1\n%2').arg(self.app.applicationName(), copyright_info))
            self.apply_wallpaper()
        self.button_refresh.setEnabled(True)

    def update_preview_size(self):
        if self.preview_pixmap.isNull():
            return
        label_size = self.lbl_image_preview.size()
        resized_pixmap = self.preview_pixmap.scaled(label_size, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.lbl_image_preview.setPixmap(resized_pixmap)

    def apply_wallpaper(self):
        """
        Slot documentation goes here.
        """
        print 'Applying wallpaper...'
        temp_path = os.path.join(tempfile.gettempdir(), 'bing_wallpaper.jpg')
        self.preview_pixmap.save(temp_path, quality=100)
        SPI_SETDESKWALLPAPER = 20  # According to http://support.microsoft.com/default.aspx?scid=97142
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, temp_path, 0)

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
        self.button_refresh.setEnabled(False)
        self.image_downloader.start()


