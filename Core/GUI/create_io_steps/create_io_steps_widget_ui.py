# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_io_steps_widget.ui'
#
# Created: Mon Jun  8 04:45:30 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateIO(object):
    def setupUi(self, CreateIO):
        CreateIO.setObjectName("CreateIO")
        CreateIO.resize(753, 369)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(CreateIO)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.groupBox = QtWidgets.QGroupBox(CreateIO)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.cbIO = QtWidgets.QComboBox(self.groupBox)
        self.cbIO.setObjectName("cbIO")
        self.verticalLayout_2.addWidget(self.cbIO)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_3.addWidget(self.label_4)
        self.edOptName = QtWidgets.QLineEdit(self.groupBox)
        self.edOptName.setObjectName("edOptName")
        self.verticalLayout_3.addWidget(self.edOptName)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.edOptType = QtWidgets.QLineEdit(self.groupBox)
        self.edOptType.setObjectName("edOptType")
        self.verticalLayout_4.addWidget(self.edOptType)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.edOptDef = QtWidgets.QLineEdit(self.groupBox)
        self.edOptDef.setObjectName("edOptDef")
        self.verticalLayout_6.addWidget(self.edOptDef)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_7.addWidget(self.label_8)
        self.btnAddOpt = QtWidgets.QPushButton(self.groupBox)
        self.btnAddOpt.setObjectName("btnAddOpt")
        self.verticalLayout_7.addWidget(self.btnAddOpt)
        self.horizontalLayout_2.addLayout(self.verticalLayout_7)
        self.verticalLayout_8.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tblOptions = QtWidgets.QTableView(CreateIO)
        self.tblOptions.setObjectName("tblOptions")
        self.horizontalLayout.addWidget(self.tblOptions)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnRemoveOpt = QtWidgets.QPushButton(CreateIO)
        self.btnRemoveOpt.setObjectName("btnRemoveOpt")
        self.verticalLayout.addWidget(self.btnRemoveOpt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_8.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.buttonBox = QtWidgets.QDialogButtonBox(CreateIO)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_5.addWidget(self.buttonBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_5)

        self.retranslateUi(CreateIO)
        QtCore.QMetaObject.connectSlotsByName(CreateIO)

    def retranslateUi(self, CreateIO):
        _translate = QtCore.QCoreApplication.translate
        CreateIO.setWindowTitle(_translate("CreateIO", "Create IO blocks"))
        self.groupBox.setTitle(_translate("CreateIO", "New option"))
        self.label_3.setText(_translate("CreateIO", "IO"))
        self.label_4.setText(_translate("CreateIO", "name"))
        self.label_5.setText(_translate("CreateIO", "type"))
        self.label_7.setText(_translate("CreateIO", "default"))
        self.btnAddOpt.setText(_translate("CreateIO", "Add option"))
        self.btnRemoveOpt.setText(_translate("CreateIO", "Remove"))
