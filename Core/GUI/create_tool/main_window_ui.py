# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Jun  3 18:02:39 2015
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(862, 632)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.edToolName = QtWidgets.QLineEdit(Form)
        self.edToolName.setObjectName("edToolName")
        self.horizontalLayout_3.addWidget(self.edToolName)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cbIO = QtWidgets.QComboBox(self.groupBox)
        self.cbIO.setObjectName("cbIO")
        self.horizontalLayout_2.addWidget(self.cbIO)
        self.edOptName = QtWidgets.QLineEdit(self.groupBox)
        self.edOptName.setObjectName("edOptName")
        self.horizontalLayout_2.addWidget(self.edOptName)
        self.edOptType = QtWidgets.QLineEdit(self.groupBox)
        self.edOptType.setObjectName("edOptType")
        self.horizontalLayout_2.addWidget(self.edOptType)
        self.edOptRepr = QtWidgets.QLineEdit(self.groupBox)
        self.edOptRepr.setObjectName("edOptRepr")
        self.horizontalLayout_2.addWidget(self.edOptRepr)
        self.edOptDef = QtWidgets.QLineEdit(self.groupBox)
        self.edOptDef.setObjectName("edOptDef")
        self.horizontalLayout_2.addWidget(self.edOptDef)
        self.btnAddOpt = QtWidgets.QPushButton(self.groupBox)
        self.btnAddOpt.setObjectName("btnAddOpt")
        self.horizontalLayout_2.addWidget(self.btnAddOpt)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tblOptions = QtWidgets.QTableView(Form)
        self.tblOptions.setObjectName("tblOptions")
        self.horizontalLayout.addWidget(self.tblOptions)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnRemoveOpt = QtWidgets.QPushButton(Form)
        self.btnRemoveOpt.setObjectName("btnRemoveOpt")
        self.verticalLayout.addWidget(self.btnRemoveOpt)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.edFormat = QtWidgets.QLineEdit(Form)
        self.edFormat.setObjectName("edFormat")
        self.horizontalLayout_4.addWidget(self.edFormat)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.btnSave = QtWidgets.QPushButton(Form)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_5.addWidget(self.btnSave)
        self.btnExit = QtWidgets.QPushButton(Form)
        self.btnExit.setObjectName("btnExit")
        self.horizontalLayout_5.addWidget(self.btnExit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Tool name"))
        self.groupBox.setTitle(_translate("Form", "New option"))
        self.btnAddOpt.setText(_translate("Form", "Add option"))
        self.btnRemoveOpt.setText(_translate("Form", "Remove"))
        self.label_2.setText(_translate("Form", "Format"))
        self.btnSave.setText(_translate("Form", "Save"))
        self.btnExit.setText(_translate("Form", "Exit"))

