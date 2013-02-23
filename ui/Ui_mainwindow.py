# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\dev\Python\Bing Wallpaper Changer\ui\mainwindow.ui'
#
# Created: Sat Feb 23 21:22:34 2013
#      by: PyQt4 UI code generator 4.9.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(649, 373)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/ui/ot_icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(self.centralWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.lbl_image_preview = ImageLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Ignored, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_preview.sizePolicy().hasHeightForWidth())
        self.lbl_image_preview.setSizePolicy(sizePolicy)
        self.lbl_image_preview.setFrameShape(QtGui.QFrame.NoFrame)
        self.lbl_image_preview.setScaledContents(False)
        self.lbl_image_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.lbl_image_preview.setObjectName(_fromUtf8("lbl_image_preview"))
        self.verticalLayout_2.addWidget(self.lbl_image_preview)
        self.lbl_image_info = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_info.sizePolicy().hasHeightForWidth())
        self.lbl_image_info.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.lbl_image_info.setFont(font)
        self.lbl_image_info.setObjectName(_fromUtf8("lbl_image_info"))
        self.verticalLayout_2.addWidget(self.lbl_image_info)
        self.lbl_image_date = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_image_date.sizePolicy().hasHeightForWidth())
        self.lbl_image_date.setSizePolicy(sizePolicy)
        self.lbl_image_date.setText(_fromUtf8(""))
        self.lbl_image_date.setObjectName(_fromUtf8("lbl_image_date"))
        self.verticalLayout_2.addWidget(self.lbl_image_date)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.button_refresh = QtGui.QPushButton(self.centralWidget)
        self.button_refresh.setObjectName(_fromUtf8("button_refresh"))
        self.horizontalLayout.addWidget(self.button_refresh)
        self.button_close = QtGui.QPushButton(self.centralWidget)
        self.button_close.setObjectName(_fromUtf8("button_close"))
        self.horizontalLayout.addWidget(self.button_close)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralWidget)
        self.actionDelete_Files = QtGui.QAction(MainWindow)
        self.actionDelete_Files.setObjectName(_fromUtf8("actionDelete_Files"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Bing Wallpaper Changer", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_image_preview.setText(QtGui.QApplication.translate("MainWindow", "Loading...", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_image_info.setText(QtGui.QApplication.translate("MainWindow", "Loading...", None, QtGui.QApplication.UnicodeUTF8))
        self.button_refresh.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.button_close.setText(QtGui.QApplication.translate("MainWindow", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete_Files.setText(QtGui.QApplication.translate("MainWindow", "Delete Files", None, QtGui.QApplication.UnicodeUTF8))

from custom_widgets import ImageLabel
import rec_rc
