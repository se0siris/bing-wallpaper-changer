from PyQt4.QtCore import QSize
from PyQt4.QtGui import QLabel, QSystemTrayIcon, QMenu, QApplication

__author__ = 'Gary'


class ImageLabel(QLabel):
    def sizeHint(self):
        return QSize(0, 192)


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.exit_action = menu.addAction('Exit')

        self.exit_action.triggered.connect(self.close_application)
        self.setContextMenu(menu)
        self.setToolTip(QApplication.instance().applicationName())

    def close_application(self):
        self.parent().close()


