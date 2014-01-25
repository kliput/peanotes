# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window.ui'
#
# Created: Sat Jan 25 23:24:27 2014
#      by: pyside-uic 0.2.13 running on PySide 1.1.0
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_PeanotesSettings(object):
    def setupUi(self, PeanotesSettings):
        PeanotesSettings.setObjectName("PeanotesSettings")
        PeanotesSettings.resize(400, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(PeanotesSettings)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.filtersList = QtGui.QListWidget(PeanotesSettings)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filtersList.sizePolicy().hasHeightForWidth())
        self.filtersList.setSizePolicy(sizePolicy)
        self.filtersList.setMaximumSize(QtCore.QSize(150, 16777215))
        self.filtersList.setObjectName("filtersList")
        self.verticalLayout.addWidget(self.filtersList)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.addButton = QtGui.QPushButton(PeanotesSettings)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout_2.addWidget(self.addButton)
        self.removeButton = QtGui.QPushButton(PeanotesSettings)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout_2.addWidget(self.removeButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label = QtGui.QLabel(PeanotesSettings)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.fromEdit = QtGui.QLineEdit(PeanotesSettings)
        self.fromEdit.setObjectName("fromEdit")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.fromEdit)
        self.label_2 = QtGui.QLabel(PeanotesSettings)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.toEdit = QtGui.QLineEdit(PeanotesSettings)
        self.toEdit.setObjectName("toEdit")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.toEdit)
        self.label_3 = QtGui.QLabel(PeanotesSettings)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.colorBox = QtGui.QComboBox(PeanotesSettings)
        self.colorBox.setObjectName("colorBox")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.colorBox)
        self.label_4 = QtGui.QLabel(PeanotesSettings)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.containsEdit = QtGui.QPlainTextEdit(PeanotesSettings)
        self.containsEdit.setObjectName("containsEdit")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.containsEdit)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.saveButton = QtGui.QPushButton(PeanotesSettings)
        self.saveButton.setObjectName("saveButton")
        self.verticalLayout_2.addWidget(self.saveButton)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(PeanotesSettings)
        QtCore.QMetaObject.connectSlotsByName(PeanotesSettings)

    def retranslateUi(self, PeanotesSettings):
        PeanotesSettings.setWindowTitle(QtGui.QApplication.translate("PeanotesSettings", "Peanotes Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.addButton.setText(QtGui.QApplication.translate("PeanotesSettings", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeButton.setText(QtGui.QApplication.translate("PeanotesSettings", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PeanotesSettings", "From:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PeanotesSettings", "To:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PeanotesSettings", "Contains:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PeanotesSettings", "Set color:", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("PeanotesSettings", "Save changes", None, QtGui.QApplication.UnicodeUTF8))

