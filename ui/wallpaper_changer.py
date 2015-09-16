from PyQt4.QtCore import QProcess
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
            print 'Setting wallpaper using environment "{0:s}"'.format(env)
            if env == 'feh':
                return self._feh(filepath)
            elif env == 'unity':
                return self._unity(filepath)
            elif env == 'xfce4':
                return self._xfce4(filepath)
            elif env == 'mate':
                return self._mate(filepath)

    def _windows(self, filepath):
        import ctypes

        SPI_SETDESKWALLPAPER = 20  # According to http://support.microsoft.com/default.aspx?scid=97142
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 0, filepath, 1)

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
                                unicode(self.process.readAllStandardOutput()))
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

