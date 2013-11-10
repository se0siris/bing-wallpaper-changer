from PyQt4.QtCore import QTimer
from PyQt4.QtGui import QMessageBox, QSpacerItem, QSizePolicy, QApplication

__author__ = 'Gary'


class TimedMessageBox(QMessageBox):

    def __init__(self, timeout=10000, parent=None):
        QMessageBox.__init__(self, parent)
        self.timeout = timeout
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.tick)
        self.timer.start()

    def tick(self):
        self.timeout -= 1000
        self.update_text()
        if not self.timeout:
            self.accept()
        else:
            self.timer.start()

    def update_text(self):
        seconds = self.timeout / 1000
        plurality = 'second' if seconds == 1 else 'seconds'
        self.button(QMessageBox.Ok).setText(' Closing in {} {}...'.format(self.timeout / 1000, plurality))


def message_box_ok(text, informative_text, title=None, icon=QMessageBox.Information, timeout=-1):
    if timeout < 0:
        msg_box = QMessageBox()
    else:
        msg_box = TimedMessageBox(timeout)

    msg_box.setText('<b>%s</b>' % text)
    if informative_text:
        msg_box.setInformativeText(informative_text)
    msg_box.setIcon(icon)
    if title:
        msg_box.setWindowTitle(title)
    else:
        msg_box.setWindowTitle(QApplication.instance().applicationName())
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setDefaultButton(QMessageBox.Ok)
    if timeout >= 0:
        msg_box.update_text()
    horizontal_spacer = QSpacerItem(400, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout = msg_box.layout()
    layout.addItem(horizontal_spacer, layout.rowCount(), 0, 1, layout.columnCount())
    return msg_box.exec_()


def message_box_error(text, informative_text, title=None, icon=QMessageBox.Critical):
    msg_box = QMessageBox()
    msg_box.setText('<b>%s</b>' % text)
    if informative_text:
        msg_box.setInformativeText(informative_text)
    msg_box.setIcon(icon)
    if title:
        msg_box.setWindowTitle(title)
    else:
        msg_box.setWindowTitle(QApplication.instance().applicationName())
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.setDefaultButton(QMessageBox.Ok)
    horizontal_spacer = QSpacerItem(400, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
    layout = msg_box.layout()
    layout.addItem(horizontal_spacer, layout.rowCount(), 0, 1, layout.columnCount())
    return msg_box.exec_()
