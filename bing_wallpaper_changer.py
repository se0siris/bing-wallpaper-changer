"""
Bing Wallpaper Changer
Copyright (c) 2013 Gary Hughes
"""

import sys

from PyQt4.QtCore import QLocale
from PyQt4.QtGui import QApplication, QStyleFactory, QIcon, QPixmap

from ui.mainwindow import MainWindow


VERSION = '1.2.0 - 26/02/2013'


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

    mainwindow = MainWindow()
    # mainwindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    startmain()

