"""
Bing Wallpaper Changer
Copyright (c) 2013 Gary Hughes
"""
import StringIO
import argparse

import sys

from PyQt4.QtCore import QLocale
from PyQt4.QtGui import QApplication, QStyleFactory, QIcon, QPixmap

from ui.mainwindow import MainWindow
from ui.message_boxes import message_box_ok


VERSION = '1.4.0 - 27/10/2013'


def parse_arguments():
    parser = argparse.ArgumentParser(description='Bing Wallpaper Changer', add_help=False)

    parser.add_argument('--quit', dest='quit', action='store_true', default=False, help='update wallpaper and exit')
    parser.add_argument('--help', dest='help', action='store_true', help='show help window')
    parser.add_argument('--version', action='version', version='Bing Wallpaper Changer %s' % VERSION)

    # Here's a dirty hack to allow argparse's errors to be displayed in a message box.
    # Re-direct stderr to a StringIO object. If argparse raises SystemExit switch stderr back from our
    # backup, rewind the StringIO and read the error from it to display in a message box before quitting.
    temp_buffer = StringIO.StringIO()
    backup_stderr = sys.stderr
    sys.stderr = temp_buffer
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.stderr = backup_stderr
        temp_buffer.seek(0)
        error = temp_buffer.read()
        message_box_ok('Bing Wallpaper Changer', error)
        sys.exit()
    sys.stderr = backup_stderr

    if args.help:
        temp_file = StringIO.StringIO()
        parser.print_help(temp_file)
        temp_file.seek(0)
        help_message = temp_file.read()
        message_box_ok('Command line options', help_message)
        sys.exit()
    return args


def startmain():
    """
    Initialise the application and display the main window.
    """
    app = QApplication(sys.argv)
    app.cleanup_files = []

    QApplication.setStyle(QStyleFactory.create('CleanLooks'))
    QApplication.setPalette(QApplication.style().standardPalette())

    QApplication.setApplicationName('Bing Wallpaper Changer')
    QApplication.setApplicationVersion(VERSION)
    QApplication.setOrganizationName('overThere.co.uk')
    QApplication.setWindowIcon(QIcon(QPixmap(':/icons/ui/ot_icon.png')))

    print 'AppName: %s' % QApplication.applicationName()
    print 'AppVersion: %s' % QApplication.applicationVersion()
    print 'Company Name: %s' % QApplication.organizationName()

    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedKingdom))

    # Add passed arguments to app.
    app.args = parse_arguments()
    print 'Args:', app.args

    mainwindow = MainWindow()
    # mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    startmain()

