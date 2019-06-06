from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMessageBox, QSpacerItem, QSizePolicy, QApplication

__author__ = 'Gary'


def message_box_ok(text, informative_text, title=None, icon=QMessageBox.Information):
    msg_box = QMessageBox()

    msg_box.setText(f'<b>{text}</b>')
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


def message_box_error(text, informative_text, title=None, icon=QMessageBox.Critical):
    msg_box = QMessageBox()
    msg_box.setText(f'<b>{text}</b>')
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
