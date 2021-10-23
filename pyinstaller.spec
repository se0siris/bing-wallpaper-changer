# -*- mode: python ; coding: utf-8 -*-
import sys
import re
import datetime
import PyInstaller.utils.win32.versioninfo as version_info

sys.path.insert(0, SPECPATH)
from bing_wallpaper_changer import VERSION_NUMBER, APP_NAME, ORG_NAME

copyright_text = f'Copyright © {datetime.date.today().year} {ORG_NAME}'
version_string = '.'.join(map(str, VERSION_NUMBER))

version = version_info.VSVersionInfo(
    ffi=version_info.FixedFileInfo(
        # filevers and prodvers should be always a tuple with four items: (1, 2, 3, 4)
        # Set not needed items to zero 0.
        filevers=VERSION_NUMBER,
        prodvers=VERSION_NUMBER,
        # Contains a bitmask that specifies the valid bits 'flags'r
        mask=0x3f,
        # Contains a bitmask that specifies the Boolean attributes of the file.
        flags=0x0,
        # The operating system for which this file was designed.
        # 0x4 - NT and there is no need to change it.
        OS=0x40004,
        # The general type of file.
        # 0x1 - the file is an application.
        fileType=0x1,
        # The function of the file.
        # 0x0 - the function is not defined for this fileType
        subtype=0x0,
        # Creation date and time stamp.
        date=(0, 0)
    ),
    kids=[
        version_info.StringFileInfo(
            [
                version_info.StringTable(
                    '040904b0',
                    [version_info.StringStruct('CompanyName', ORG_NAME),
                     version_info.StringStruct('FileDescription', APP_NAME),
                     version_info.StringStruct('FileVersion', version_string),
                     version_info.StringStruct('InternalName', APP_NAME),
                     version_info.StringStruct('LegalCopyright', copyright_text),
                     version_info.StringStruct('OriginalFilename', f'{APP_NAME}.exe'),
                     version_info.StringStruct('ProductName', f'{APP_NAME}.exe'),
                     version_info.StringStruct('ProductVersion', version_string)])
            ]),
        version_info.VarFileInfo(
            [version_info.VarStruct('Translation', [1033, 1200])]
        )
    ]
)

excludes = (
    'numpy', 'pywin', 'tcl', 'tk', 'Tkinter', '_tkinter', 'test', 'lib2to3', 'Include',
    'ImageTk', 'PIL._imagingtk', 'PyInstaller', '_hashlib', '_ssl', 'bz2', '_bsddb',
    'PIL', 'asyncio', 'lzma', 'decimal', 'multiprocessing', 'queue', 'pyconfig'
)

block_cipher = None
a = Analysis(
    ['bing_wallpaper_changer.py'],
    pathex=[SPECPATH],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

# Exclude DLLs that aren't needed.
ex_plugins = (
    'd3dcompiler', 'libeay32', 'libegl', 'libgles', 'opengl', 'ssleay32', 'genericbearer', 'qgif', 'qicns',
    'qico', 'qtga', 'qtiff', 'qwbmp', 'qwebp', 'qminimal', 'qoffscreen', 'qwebgl', 'qxdgdesktopportal',
    'qsqlmysql', 'qsqlodbc', 'qsqlpsql', 'qwindowsvistastyle', 'qtbase_', 'libcrypto', 'libssl', 'dbus',
    '5qml', '5quick', '5websockets', 'api-ms-win'
)
regex_plugin_filter = re.compile(r'^.*(?:{0:s}).*$'.format('|'.join(ex_plugins)))

a.binaries = [x for x in a.binaries if not regex_plugin_filter.match(x[0].lower())]
a.datas = [x for x in a.datas if not regex_plugin_filter.match(x[0].lower())]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name=APP_NAME,
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False,
          icon=r'c:\dev\Graphics\Icons\man_icon.ico',
          version=version
          )

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=APP_NAME
)
