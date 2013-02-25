from PyQt4.QtCore import QSize
from PyQt4.QtGui import QLabel, QSystemTrayIcon, QMenu, QApplication

__author__ = 'Gary'


class ImageLabel(QLabel):
    def sizeHint(self):
        return QSize(0, 0)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.settings_action = menu.addAction('&Settings')
        self.exit_action = menu.addAction('E&xit')

        self.settings_action.triggered.connect(self.show_settings)
        self.exit_action.triggered.connect(self.close_application)
        self.setContextMenu(menu)
        self.setToolTip(QApplication.instance().applicationName())

    def show_settings(self):
        self.parent().tabWidget.setCurrentIndex(1)
        self.parent().show()
        self.parent().setFocus()

    def close_application(self):
        self.parent().close()


