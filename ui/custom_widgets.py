from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QLabel, QSystemTrayIcon, QMenu, QApplication, QListWidgetItem

__author__ = 'Gary'


class ImageLabel(QLabel):
    """
    Custom label with hardcoded sizeHint() to prevent weird resizing issues.
    """

    def sizeHint(self):
        return QSize(0, 0)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super(SystemTrayIcon, self).__init__(icon, parent)

        self.mainwindow = parent

        menu = QMenu()
        self.settings_action = menu.addAction('&Settings')
        self.exit_action = menu.addAction('E&xit')

        self.settings_action.triggered.connect(self.show_settings)
        self.exit_action.triggered.connect(self.close_application)
        self.setContextMenu(menu)
        self.setToolTip(QApplication.applicationName())

    @pyqtSlot()
    def show_settings(self):
        self.mainwindow.tabWidget.setCurrentIndex(1)
        self.mainwindow.show()
        self.mainwindow.setFocus()

    @pyqtSlot()
    def close_application(self):
        self.mainwindow.close()
