import os

from PyQt5.QtCore import QProcess
from ui.settings import Settings
import re
import platform

__author__ = 'gary'


class WallpaperChanger(object):
    def __init__(self):
        self.settings = Settings()
        self.process = QProcess()

    def apply_wallpaper(self, filepath):
        system_platform = platform.system()
        if system_platform == 'Windows':
            return self._windows(filepath)
        elif system_platform == 'Linux':
            # Read desktop environment from settings.
            env = self.settings.linux_desktop
            print('Setting wallpaper using environment "{0:s}"'.format(env))
            if env == 'feh':
                return self._feh(filepath)
            elif env == 'unity':
                return self._unity(filepath)
            elif env == 'xfce4':
                return self._xfce4(filepath)
            elif env == 'mate':
                return self._mate(filepath)
            elif env == 'kde4':
                return self._kde4(filepath)
            elif env == 'cinnamon':
                return self._cinnamon(filepath)

    def _windows(self, filepath):
        import ctypes

        SPI_SETDESKWALLPAPER = 0x14  # According to http://support.microsoft.com/default.aspx?scid=97142
        SPIF_UPDATEINIFILE = 0x2
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, SPIF_UPDATEINIFILE)

    def _feh(self, filepath):
        error = self.process.execute('feh --bg-scale {0:s}'.format(filepath))
        return not bool(error)

    def _unity(self, filepath):
        error = self.process.execute('gsettings set org.gnome.desktop.background picture-uri {0:s}'.format(filepath))
        return not bool(error)

    def _mate(self, filepath):
        error = self.process.execute('gsettings set org.mate.background picture-filename {0:s}'.format(filepath))
        return not bool(error)

    def _xfce4(self, filepath):
        self.process.start('xfconf-query -c xfce4-desktop -l')
        self.process.waitForFinished()
        properties = re.findall(r'(/backdrop/screen.*(?:last-image|image-path))',
                                str(self.process.readAllStandardOutput()))
        error = False
        for item in properties:
            self.process.start('xfconf-query --channel xfce4-desktop --property {0:s} --set {1:s}'.format(item, '/'))
            self.process.waitForFinished()
            self.process.start(
                'xfconf-query --channel xfce4-desktop --property {0:s} --set {1:s}'.format(item, filepath))
            self.process.waitForFinished()
            if self.process.exitCode():
                error = True
        return not error

    def _kde4(self, filepath):
        kde4_js = '''
var wallpaper = "{0:s}";
var activity = activities()[0];
activity.currentConfigGroup = ["Wallpaper","image"];
activity.writeConfig("wallpaper", wallpaper);
activity.writeConfig("userswallpaper", wallpaper);
activity.reloadConfig();
        '''.format(filepath)
        kde4_js_path = '/tmp/bwc_kde4_js'
        with open(kde4_js_path, 'w') as kde4_js_file:
            kde4_js_file.write(kde4_js)

        self.process.start('qdbus', ['org.kde.plasma-desktop', '/MainApplication', 'loadScriptInInteractiveConsole',
                                     kde4_js_path])
        self.process.waitForFinished()
        os.remove(kde4_js_path)

        self.process.start('dbus-send',
                           ['--dest=org.kde.plasma-desktop', '/MainApplication',
                            'org.kde.plasma-desktop.reparseConfiguration'])
        self.process.waitForFinished()
        self.process.start('dbus-send',
                           ['--dest=org.freedesktop.DBus', '/org/freedesktop/DBus',
                            'org.freedesktop.DBus.ReloadConfig'])
        self.process.waitForFinished()
        self.process.start('dbus-send',
                           ['--dest=org.kde.kwin', '/KWin', 'org.kde.KWin.reloadConfig'])
        self.process.waitForFinished()

        self.process.start('kbuildsycoca4')
        self.process.waitForFinished()
        self.process.start('kquitapp', ['plasma-desktop'])
        self.process.waitForFinished()
        self.process.start('kstart', ['plasma-desktop'])

    def _cinnamon(self, filepath):
        error = self.process.execute('gsettings set org.cinnamon.desktop.background picture-uri "file://{0:s}"'.format(filepath))
        return not bool(error)
