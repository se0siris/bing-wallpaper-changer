"""
Bing Wallpaper Changer
Copyright (c) 2020 Gary Hughes
"""
import getpass
import struct
import time
from io import BytesIO, StringIO
import argparse
import os
import subprocess
import traceback

import sys
import platform

from PyQt5.QtCore import QLocale, QSharedMemory
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QIcon
import signal

from ui.mainwindow import MainWindow
from ui.message_boxes import message_box_ok, message_box_error


VERSION_NUMBER = (2, 0, 3, 0)
VERSION_STRING = '.'.join(map(str, VERSION_NUMBER[:-1]))
APP_NAME = 'Bing Wallpaper Changer'
ORG_NAME = 'overThere.co.uk'


def except_hook(cls, exception, tb):
    separator = '-' * 70
    log_file = 'error.log'
    time_string = time.strftime('%Y-%m-%d, %H:%M:%S')
    machine_name = platform.node()
    user_name = getpass.getuser()

    tb_info_file = StringIO()
    traceback.print_tb(tb, None, tb_info_file)
    tb_info_file.seek(0)
    tb_info = tb_info_file.read()
    error_message = '{0:s}: \n{1:s}'.format(str(cls), str(exception))
    sections = [
        separator, time_string,
        f'Username: {user_name:s}',
        f'Machine: {machine_name:s}',
        f'Version: {VERSION_STRING:s}',
        separator, error_message,
        separator, tb_info
    ]
    msg = '\n'.join(sections)
    separator = os.linesep * 4 if os.path.isfile(log_file) else ''
    try:
        with open(log_file, 'a') as f:
            f.write(separator)
            f.write(msg)
    except IOError:
        pass

    sys.__excepthook__(cls, exception, traceback)


def parse_arguments():
    parser = argparse.ArgumentParser(description=APP_NAME, add_help=False)

    parser.add_argument('--quit', dest='quit', action='store_true', default=False, help='update wallpaper and exit')
    parser.add_argument('--quit-existing', dest='quit_existing', action='store_true', default=False,
                        help='close already running process')
    parser.add_argument('--native-style', dest='native_style', action='store_true', default=False,
                        help='use native UI style')
    parser.add_argument('--help', dest='help', action='store_true', help='show help window')
    parser.add_argument('--version', action='version', version=f'{APP_NAME} {VERSION_STRING}')

    # Here's a dirty hack to allow argparse's errors to be displayed in a message box.
    # Re-direct stderr to a StringIO object. If argparse raises SystemExit switch stderr back from our
    # backup, rewind the StringIO and read the error from it to display in a message box before quitting.
    temp_buffer = BytesIO()
    backup_stderr = sys.stderr
    sys.stderr = temp_buffer
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.stderr = backup_stderr
        temp_buffer.seek(0)
        error = temp_buffer.read()
        message_box_ok(APP_NAME, error)
        sys.exit()
    sys.stderr = backup_stderr

    if args.help:
        temp_file = BytesIO()
        parser.print_help(temp_file)
        temp_file.seek(0)
        help_message = temp_file.read()
        message_box_ok('Command line options', help_message)
        sys.exit()
    return args


def instance_check(app):
    app.instance_check = QSharedMemory(f'{APP_NAME} - Instance Check')
    if not app.instance_check.create(4, QSharedMemory.ReadWrite):
        # Already running. Read the PID from the shared memory and return it.
        app.instance_check.attach(QSharedMemory.ReadOnly)

        app.instance_check.lock()
        view = memoryview(app.instance_check.data())
        existing_pid = struct.unpack('=i', view[:4])[0]
        app.instance_check.unlock()
        return existing_pid

    # Write the current PID into the shared memory object.
    pid = app.applicationPid()
    app.instance_check.lock()
    app.instance_check.data()[:4] = memoryview(struct.pack('=i', pid))
    app.instance_check.unlock()
    return 0


def startmain():
    """
    Initialise the application and display the main window.
    """
    args = parse_arguments()

    app = QApplication(sys.argv)
    app.cleanup_files = []

    if not args.native_style:
        app.setStyle(QStyleFactory.create('Fusion'))
        app.setPalette(QApplication.style().standardPalette())

    app_icon = QIcon(':/icons/ui/ot_icon.svg')
    print(app_icon.isNull(), app_icon.pixmap(200, 200).isNull())

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION_STRING)
    app.setOrganizationName(ORG_NAME)
    app.setWindowIcon(app_icon)

    print('AppName: {0:s}'.format(app.applicationName()))
    print('AppVersion: {0:s}'.format(app.applicationVersion()))
    print('Company Name: {0:s}'.format(app.organizationName()))

    QLocale.setDefault(QLocale(QLocale.English, QLocale.UnitedKingdom))

    # Add passed arguments to app.
    app.args = args
    print('Args:', app.args)

    # Check to see if application already running.
    existing_pid = instance_check(app)
    if existing_pid:
        print(existing_pid)
        if app.args.quit_existing:
            # Command line argument passed to close existing program. Do that, then quit.
            if platform.system() == "Windows":
                subprocess.Popen("taskkill /F /T /PID %i" % existing_pid, shell=True)
            else:
                os.killpg(existing_pid, signal.SIGKILL)
        else:
            message_box_error(
                'Program already running.',
                'You can only have one copy of the Bing Wallpaper Changer running at once.'
            )
        sys.exit()

    mainwindow = MainWindow()
    sys.exit(app.exec())


if __name__ == "__main__":
    sys.excepthook = except_hook
    startmain()
