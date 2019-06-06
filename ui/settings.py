import os
from PyQt5.QtCore import QSettings, QStandardPaths

__author__ = 'Gary Hughes'


class Settings(object):
    """
    Wrapper for the settings file to get/set values.
    """

    def __init__(self):
        settings_folder = QStandardPaths.writableLocation(QStandardPaths.DataLocation)
        if not os.path.isdir(settings_folder):
            os.makedirs(settings_folder)
        settings_path = os.path.join(settings_folder, 'settings.ini')
        print(settings_path)
        self.settings = QSettings(settings_path, QSettings.IniFormat)

    @property
    def image_resolution(self):
        return self.settings.value('Image/resolution', 3, type=int)

    @image_resolution.setter
    def image_resolution(self, resolution):
        """
        Set image resolution (0: 1024x768, 1: 1280x720, 2: 1366x768, 3: 1920x1200).
        :type resolution: int
        """
        self.settings.setValue('Image/resolution', resolution)

    @property
    def auto_update_enabled(self):
        return self.settings.value('Automatic_update/enabled', True, type=bool)

    @auto_update_enabled.setter
    def auto_update_enabled(self, enabled):
        """
        Enable automatic updates.
        :type enabled: bool
        """
        self.settings.setValue('Automatic_update/enabled', enabled)

    @property
    def auto_update_interval(self):
        return self.settings.value('Automatic_update/interval', 1200000, type=int)

    @auto_update_interval.setter
    def auto_update_interval(self, interval):
        """
        Specify interval for update checks in milliseconds.
        :type interval: int
        """
        self.settings.setValue('Automatic_update/interval', interval)

    @property
    def run_command_enabled(self):
        return self.settings.value('Run_command/enabled', False, type=bool)

    @run_command_enabled.setter
    def run_command_enabled(self, enabled):
        """
        Run a command after the wallpaper has been changed.
        :type enabled: bool
        """
        self.settings.setValue('Run_command/enabled', enabled)

    @property
    def run_command_command(self):
        return self.settings.value('Run_command/command', '')

    @run_command_command.setter
    def run_command_command(self, command_string):
        """
        Command to run after changing the wallpaper.
        :type command_string: str
        """
        self.settings.setValue('Run_command/command', command_string)

    @property
    def archive_enabled(self):
        return self.settings.value('Archive/enabled', False, type=bool)

    @archive_enabled.setter
    def archive_enabled(self, enabled):
        """
        Save a copy of downloaded wallpapers.
        :type enabled: bool
        """
        self.settings.setValue('Archive/enabled', enabled)

    @property
    def archive_location(self):
        return self.settings.value('Archive/location', '')

    @archive_location.setter
    def archive_location(self, command_string):
        """
        Location to store saved wallpapers.
        :type command_string: str
        """
        self.settings.setValue('Archive/location', command_string)

    @property
    def icon_colour(self):
        return self.settings.value('GUI/icon_colour', type=int)

    @icon_colour.setter
    def icon_colour(self, icon_colour):
        """
        Colour of the icon to use in the system tray.
        :param icon_colour: 0 = black, 1 = white
        :type icon_colour: int
        """
        self.settings.setValue('GUI/icon_colour', icon_colour)

    @property
    def linux_desktop(self):
        return self.settings.value('Linux/desktop', 'unity')

    @linux_desktop.setter
    def linux_desktop(self, value):
        if value == 0:
            self.settings.setValue('Linux/desktop', 'unity')
        elif value == 1:
            self.settings.setValue('Linux/desktop', 'mate')
        elif value == 2:
            self.settings.setValue('Linux/desktop', 'xfce4')
        elif value == 3:
            self.settings.setValue('Linux/desktop', 'feh')
        elif value == 4:
            self.settings.setValue('Linux/desktop', 'kde4')
        elif value == 5:
            self.settings.setValue('Linux/desktop', 'cinnamon')
