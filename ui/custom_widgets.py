from PyQt4.QtCore import QSize, QDate
from PyQt4.QtGui import QLabel, QSystemTrayIcon, QMenu, QApplication, QListWidgetItem

__author__ = 'Gary'


def text_to_date(text):
    text = '{} {}'.format(str(text), str(QDate.currentDate().year()))
    return QDate.fromString(text, 'dddd dd MMMM yyyy')


class ImageLabel(QLabel):
    """
    Custom label with hardcoded sizeHint() to prevent weird resizing issues.
    """

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


class ListWidgetItem(QListWidgetItem):
    """
    Custom QListWidgetItem to provide custom sorting for items with a QDate.
    """

    def __le__(self, b):
        return b.image_date <= self.image_date

    def __lt__(self, b):
        return b.image_date < self.image_date

    def __gt__(self, b):
        return b.image_date > self.image_date

    def __ge__(self, b):
        return b.image_date >= self.image_date

    def __eq__(self, b):
        return b.image_date == self.image_date

    def __ne__(self, b):
        return b.image_date != self.image_date
