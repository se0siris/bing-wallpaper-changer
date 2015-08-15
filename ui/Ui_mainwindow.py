# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\Bing Wallpaper Changer\ui\mainwindow.ui'
#
# Created: Sat Aug 15 17:04:52 2015
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(717, 385)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/ui/ot_icon.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralWidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_preview = QtGui.QWidget()
        self.tab_preview.setObjectName(_fromUtf8("tab_preview"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab_preview)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lbl_image_preview = ImageLabel(self.tab_preview)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_preview.sizePolicy().hasHeightForWidth())
        self.lbl_image_preview.setSizePolicy(sizePolicy)
        self.lbl_image_preview.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbl_image_preview.setScaledContents(False)
        self.lbl_image_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image_preview.setObjectName(_fromUtf8("lbl_image_preview"))
        self.verticalLayout.addWidget(self.lbl_image_preview)
        self.lbl_image_info = QtGui.QLabel(self.tab_preview)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_info.sizePolicy().hasHeightForWidth())
        self.lbl_image_info.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_image_info.setFont(font)
        self.lbl_image_info.setWordWrap(True)
        self.lbl_image_info.setObjectName(_fromUtf8("lbl_image_info"))
        self.verticalLayout.addWidget(self.lbl_image_info)
        self.lbl_image_date = QtGui.QLabel(self.tab_preview)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_date.sizePolicy().hasHeightForWidth())
        self.lbl_image_date.setSizePolicy(sizePolicy)
        self.lbl_image_date.setText(_fromUtf8(""))
        self.lbl_image_date.setWordWrap(True)
        self.lbl_image_date.setObjectName(_fromUtf8("lbl_image_date"))
        self.verticalLayout.addWidget(self.lbl_image_date)
        self.tabWidget.addTab(self.tab_preview, _fromUtf8(""))
        self.tab_settings = QtGui.QWidget()
        self.tab_settings.setObjectName(_fromUtf8("tab_settings"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.tab_settings)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.tab_settings)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        spacerItem = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.cb_resolution = QtGui.QComboBox(self.tab_settings)
        self.cb_resolution.setObjectName(_fromUtf8("cb_resolution"))
        self.cb_resolution.addItem(_fromUtf8(""))
        self.cb_resolution.addItem(_fromUtf8(""))
        self.cb_resolution.addItem(_fromUtf8(""))
        self.cb_resolution.addItem(_fromUtf8(""))
        self.horizontalLayout_4.addWidget(self.cb_resolution)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem1)
        self.cb_auto_update = QtGui.QCheckBox(self.tab_settings)
        self.cb_auto_update.setChecked(True)
        self.cb_auto_update.setObjectName(_fromUtf8("cb_auto_update"))
        self.verticalLayout_3.addWidget(self.cb_auto_update)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem2 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label = QtGui.QLabel(self.tab_settings)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.sb_update_interval = QtGui.QSpinBox(self.tab_settings)
        self.sb_update_interval.setMinimum(1)
        self.sb_update_interval.setMaximum(1440)
        self.sb_update_interval.setProperty("value", 20)
        self.sb_update_interval.setObjectName(_fromUtf8("sb_update_interval"))
        self.horizontalLayout_2.addWidget(self.sb_update_interval)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem3 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem3)
        self.cb_run_command = QtGui.QCheckBox(self.tab_settings)
        self.cb_run_command.setChecked(True)
        self.cb_run_command.setObjectName(_fromUtf8("cb_run_command"))
        self.verticalLayout_3.addWidget(self.cb_run_command)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.label_2 = QtGui.QLabel(self.tab_settings)
        self.label_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.le_command = QtGui.QLineEdit(self.tab_settings)
        self.le_command.setObjectName(_fromUtf8("le_command"))
        self.horizontalLayout_3.addWidget(self.le_command)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        spacerItem5 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem5)
        self.cb_enable_archive = QtGui.QCheckBox(self.tab_settings)
        self.cb_enable_archive.setChecked(True)
        self.cb_enable_archive.setObjectName(_fromUtf8("cb_enable_archive"))
        self.verticalLayout_3.addWidget(self.cb_enable_archive)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        spacerItem6 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem6)
        self.label_6 = QtGui.QLabel(self.tab_settings)
        self.label_6.setMinimumSize(QtCore.QSize(50, 0))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_6.addWidget(self.label_6)
        self.le_archive_location = QtGui.QLineEdit(self.tab_settings)
        self.le_archive_location.setObjectName(_fromUtf8("le_archive_location"))
        self.horizontalLayout_6.addWidget(self.le_archive_location)
        self.button_archive_browse = QtGui.QPushButton(self.tab_settings)
        self.button_archive_browse.setObjectName(_fromUtf8("button_archive_browse"))
        self.horizontalLayout_6.addWidget(self.button_archive_browse)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        spacerItem7 = QtGui.QSpacerItem(20, 10, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.verticalLayout_3.addItem(spacerItem7)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_9 = QtGui.QLabel(self.tab_settings)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_7.addWidget(self.label_9)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        spacerItem8 = QtGui.QSpacerItem(25, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem8)
        self.rb_icon_colour_black = QtGui.QRadioButton(self.tab_settings)
        self.rb_icon_colour_black.setChecked(True)
        self.rb_icon_colour_black.setObjectName(_fromUtf8("rb_icon_colour_black"))
        self.horizontalLayout_7.addWidget(self.rb_icon_colour_black)
        self.rb_icon_colour_white = QtGui.QRadioButton(self.tab_settings)
        self.rb_icon_colour_white.setObjectName(_fromUtf8("rb_icon_colour_white"))
        self.horizontalLayout_7.addWidget(self.rb_icon_colour_white)
        spacerItem9 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem9)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.verticalLayout_3.addLayout(self.verticalLayout_7)
        spacerItem10 = QtGui.QSpacerItem(20, 226, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem10)
        self.tabWidget.addTab(self.tab_settings, _fromUtf8(""))
        self.tab_history = QtGui.QWidget()
        self.tab_history.setObjectName(_fromUtf8("tab_history"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.tab_history)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.lw_wallpaper_history = ListWidget(self.tab_history)
        self.lw_wallpaper_history.setDragDropMode(QtGui.QAbstractItemView.NoDragDrop)
        self.lw_wallpaper_history.setVerticalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lw_wallpaper_history.setHorizontalScrollMode(QtGui.QAbstractItemView.ScrollPerPixel)
        self.lw_wallpaper_history.setMovement(QtGui.QListView.Static)
        self.lw_wallpaper_history.setResizeMode(QtGui.QListView.Adjust)
        self.lw_wallpaper_history.setSpacing(5)
        self.lw_wallpaper_history.setViewMode(QtGui.QListView.IconMode)
        self.lw_wallpaper_history.setUniformItemSizes(True)
        self.lw_wallpaper_history.setObjectName(_fromUtf8("lw_wallpaper_history"))
        self.verticalLayout_4.addWidget(self.lw_wallpaper_history)
        self.tabWidget.addTab(self.tab_history, _fromUtf8(""))
        self.tab_about = QtGui.QWidget()
        self.tab_about.setObjectName(_fromUtf8("tab_about"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.tab_about)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_4 = QtGui.QLabel(self.tab_about)
        self.label_4.setText(_fromUtf8(""))
        self.label_4.setPixmap(QtGui.QPixmap(_fromUtf8(":/icons/ui/ot_icon.svg")))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_5.addWidget(self.label_4)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.label_5 = QtGui.QLabel(self.tab_about)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_5.addWidget(self.label_5)
        self.lbl_version = QtGui.QLabel(self.tab_about)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lbl_version.setFont(font)
        self.lbl_version.setObjectName(_fromUtf8("lbl_version"))
        self.verticalLayout_5.addWidget(self.lbl_version)
        self.label_7 = QtGui.QLabel(self.tab_about)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_5.addWidget(self.label_7)
        self.horizontalLayout_5.addLayout(self.verticalLayout_5)
        spacerItem11 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem11)
        self.verticalLayout_6.addLayout(self.horizontalLayout_5)
        self.label_8 = QtGui.QLabel(self.tab_about)
        self.label_8.setTextFormat(QtCore.Qt.RichText)
        self.label_8.setWordWrap(True)
        self.label_8.setOpenExternalLinks(True)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_6.addWidget(self.label_8)
        self.tabWidget.addTab(self.tab_about, _fromUtf8(""))
        self.verticalLayout_2.addWidget(self.tabWidget)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_status = QtGui.QLabel(self.centralWidget)
        self.lbl_status.setObjectName(_fromUtf8("lbl_status"))
        self.horizontalLayout.addWidget(self.lbl_status)
        spacerItem12 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem12)
        self.button_refresh = QtGui.QPushButton(self.centralWidget)
        self.button_refresh.setObjectName(_fromUtf8("button_refresh"))
        self.horizontalLayout.addWidget(self.button_refresh)
        self.button_close = QtGui.QPushButton(self.centralWidget)
        self.button_close.setObjectName(_fromUtf8("button_close"))
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionDelete_Files = QtGui.QAction(MainWindow)
        self.actionDelete_Files.setObjectName(_fromUtf8("actionDelete_Files"))
        self.label_3.setBuddy(self.cb_resolution)
        self.label.setBuddy(self.sb_update_interval)
        self.label_2.setBuddy(self.le_command)
        self.label_6.setBuddy(self.le_archive_location)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.cb_resolution.setCurrentIndex(3)
        QtCore.QObject.connect(self.cb_auto_update, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.sb_update_interval.setEnabled)
        QtCore.QObject.connect(self.cb_auto_update, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label.setEnabled)
        QtCore.QObject.connect(self.cb_run_command, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_2.setEnabled)
        QtCore.QObject.connect(self.cb_run_command, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.le_command.setEnabled)
        QtCore.QObject.connect(self.cb_enable_archive, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.label_6.setEnabled)
        QtCore.QObject.connect(self.cb_enable_archive, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.le_archive_location.setEnabled)
        QtCore.QObject.connect(self.cb_enable_archive, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.button_archive_browse.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Bing Wallpaper Changer", None))
        self.lbl_image_preview.setText(_translate("MainWindow", "Loading...", None))
        self.lbl_image_info.setText(_translate("MainWindow", "Loading...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_preview), _translate("MainWindow", "Preview", None))
        self.label_3.setText(_translate("MainWindow", "Wallpaper resolution", None))
        self.cb_resolution.setItemText(0, _translate("MainWindow", "1024x768", None))
        self.cb_resolution.setItemText(1, _translate("MainWindow", "1280x720", None))
        self.cb_resolution.setItemText(2, _translate("MainWindow", "1366x768", None))
        self.cb_resolution.setItemText(3, _translate("MainWindow", "1920x1200", None))
        self.cb_auto_update.setText(_translate("MainWindow", "Automatically update wallpaper", None))
        self.label.setText(_translate("MainWindow", "Check for updates every:", None))
        self.sb_update_interval.setSuffix(_translate("MainWindow", " minutes", None))
        self.cb_run_command.setText(_translate("MainWindow", "Run command after changing wallpaper", None))
        self.label_2.setText(_translate("MainWindow", "Command:", None))
        self.cb_enable_archive.setText(_translate("MainWindow", "Keep a copy of images", None))
        self.label_6.setText(_translate("MainWindow", "Location:", None))
        self.button_archive_browse.setText(_translate("MainWindow", "Browse", None))
        self.label_9.setText(_translate("MainWindow", "Icon colour", None))
        self.rb_icon_colour_black.setText(_translate("MainWindow", "Black", None))
        self.rb_icon_colour_white.setText(_translate("MainWindow", "White", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_settings), _translate("MainWindow", "Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_history), _translate("MainWindow", "History", None))
        self.label_5.setText(_translate("MainWindow", "Bing Wallpaper Changer", None))
        self.lbl_version.setText(_translate("MainWindow", "Version %", None))
        self.label_7.setText(_translate("MainWindow", "Copyright © 2013 Gary Hughes, overThere.co.uk", None))
        self.label_8.setText(_translate("MainWindow", "<html><head/><body><p>This program is released under the GPL v3 and all source can be downloaded from:</p><p><a href=\"https://bitbucket.org/gary_hughes/bing-wallpaper-changer\"><span style=\" text-decoration: underline; color:#0000ff;\">https://bitbucket.org/gary_hughes/bing-wallpaper-changer</span></a></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), _translate("MainWindow", "About", None))
        self.lbl_status.setText(_translate("MainWindow", "CURRENT STATUS", None))
        self.button_refresh.setText(_translate("MainWindow", "Refresh", None))
        self.button_close.setText(_translate("MainWindow", "Close", None))
        self.actionDelete_Files.setText(_translate("MainWindow", "Delete Files", None))

from custom_widgets import ImageLabel, ListWidget
import rec_rc
