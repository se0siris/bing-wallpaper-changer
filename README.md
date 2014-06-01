# Bing Wallpaper Changer #

### About ###
This program will run in the  system tray and check for a new daily Bing image on a user defined interval. If the URL for the image has changed since the last check the new image will be downloaded and applied as the current wallpaper.

There is also the option to run a command after the wallpaper has been applied. This is useful for anyone that uses software that overlays data onto their wallpaper, Such as [BgInfo](echnet.microsoft.com/en-gb/sysinternals/bb897557.aspx "BgInfo") from Sysinternals.

The last two week's worth of images is available on a `History` tab - just double click a thumbnail to apply a wallpaper. If using this and you want to keep an old wallpaper don't forget to disable to the automatic updating from the main `Settings` tab, otherwise the wallpaper will be replaced with the daily wallpaper on the next update check.

### Why? ###
I don't use Bing as a search engine, but I do very much like their daily images. I was excited when I first heard about the official [Bing Desktop](http://www.bing.com/explore/desktop "Bing Desktop") application, but wasn't keen on the toolbar that was added to my desktop. I tried to just live with it for a while but it caused problems with a few full screen applications when it refreshed.

After not being able to find a similar program with the features I wanted I decided to write my own.

### Changelog ###

##### 1.5 #####
  - Ability to save images to a custom folder.
  - Increased `History` tab range back up to 3 weeks; duplicate dates will be ignored.

##### 1.4 #####
  - Command line switches for closing after applying wallpaper (--quit).

##### 1.3 #####
  - Added ability to set old Bing wallpapers from the ``History`` tab by double clicking the thumbnail.
  - Reduced ``History`` tab range from three weeks to two as duplicates were shown when Bing had featured interactive images on the homepage.

##### 1.2 #####
  - Added option to system tray menu to directly open settings page.
  - Wallpaper change is now permanent and should be retained after logoff/shutdown.
  - Switched to Qt downloading methods instead of Python.
  - Initial Linux support added in source. Tested on Ubuntu 13.04 - working fine apart from ``QSystemTrayIcon`` not being displayed. Need to find how that's handled in Ubuntu now...

##### 1.1 #####
  - Added ``Settings`` and ``History`` tabs to the main window.
  - Fixed broken refresh when current Bing image is the same as previously downloaded image.
  - GUI fixes.

##### 1.0 #####
  - First release with basic functionality.