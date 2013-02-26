import os
from PyQt4.QtCore import QSettings, QVariant
from PyQt4.QtGui import QDesktopServices

__author__ = 'Gary Hughes'


class Settings(object):
    """
    Wrapper for the settings file to get/set values.
    """

    # Retrieve values.

    def __init__(self):
        settings_folder = str(QDesktopServices.storageLocation(QDesktopServices.DataLocation))
        if not os.path.isdir(settings_folder):
            os.makedirs(settings_folder)
        settings_path = os.path.join(settings_folder, 'settings.ini')
        print settings_path
        self.settings = QSettings(settings_path, QSettings.IniFormat)

    def get_image_resolution(self):
        return self.settings.value('Image/resolution', QVariant(3)).toInt()[0]

    def get_auto_update_enabled(self):
        return self.settings.value('Automatic_update/enabled', QVariant(True)).toBool()

    def get_auto_update_interval(self):
        return self.settings.value('Automatic_update/interval', QVariant(1200000)).toInt()[0]

    def get_run_command_enabled(self):
        return self.settings.value('Run_command/enabled', QVariant(False)).toBool()

    def get_run_command_command(self):
        return self.settings.value('Run_command/command', QVariant('')).toString()

    # Set values.

    def set_image_resolution(self, resolution):
        """
        Set image resolution (0: 1024x768, 1: 1280x720, 2: 1366x768, 3: 1920x1200).
        :type resolution: int
        """
        self.settings.setValue('Image/resolution', resolution)

    def set_auto_update_enabled(self, enabled):
        """
        Enable automatic updates.
        :type enabled: bool
        """
        self.settings.setValue('Automatic_update/enabled', enabled)

    def set_auto_update_interval(self, interval):
        """
        Specify interval for update checks in milliseconds.
        :type interval: int
        """
        self.settings.setValue('Automatic_update/interval', interval)

    def set_run_command_enabled(self, enabled):
        """
        Run a command after the wallpaper has been changed.
        :type enabled: bool
        """
        self.settings.setValue('Run_command/enabled', enabled)

    def set_run_command_command(self, command_string):
        """
        Command to run after changing the wallpaper.
        :type command_string: str
        """
        self.settings.setValue('Run_command/command', command_string)
