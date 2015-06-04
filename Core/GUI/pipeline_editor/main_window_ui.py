# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Thu Jun  4 03:35:05 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(913, 828)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.edFilter = QtWidgets.QLineEdit(self.groupBox)
        self.edFilter.setObjectName("edFilter")
        self.verticalLayout.addWidget(self.edFilter)
        self.lstTools = QtWidgets.QListView(self.groupBox)
        self.lstTools.setObjectName("lstTools")
        self.verticalLayout.addWidget(self.lstTools)
        self.btnAddStep = QtWidgets.QPushButton(self.groupBox)
        self.btnAddStep.setObjectName("btnAddStep")
        self.verticalLayout.addWidget(self.btnAddStep)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listView = QtWidgets.QListView(self.groupBox_2)
        self.listView.setObjectName("listView")
        self.verticalLayout_2.addWidget(self.listView)
        self.btnConnect = QtWidgets.QPushButton(self.groupBox_2)
        self.btnConnect.setObjectName("btnConnect")
        self.verticalLayout_2.addWidget(self.btnConnect)
        self.verticalLayout_3.addWidget(self.groupBox_2)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.areaLayout = QtWidgets.QVBoxLayout()
        self.areaLayout.setObjectName("areaLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.areaLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.areaLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 913, 20))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pipeline editor"))
        self.groupBox.setTitle(_translate("MainWindow", "Tools"))
        self.btnAddStep.setText(_translate("MainWindow", "Add"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Properties"))
        self.btnConnect.setText(_translate("MainWindow", "Connect"))
        self.menuHelp.setTitle(_translate("MainWindow", "help"))
        self.actionAbout.setText(_translate("MainWindow", "About"))

