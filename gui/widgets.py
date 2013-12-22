# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtGui import QPushButton, QHBoxLayout, QWidget

from gui.utils import pea_app

class UserEntry(QPushButton):
    def __init__(self, name, parent=None):
        super(UserEntry, self).__init__(name, parent)
    def userName(self):
        return self.text()
        

class ToolBar(QWidget):
    def __init__(self, parent=None):
        super(ToolBar, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(QHBoxLayout())
        
        iconButtonPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        iconButtonPolicy.setHorizontalStretch(0)
        iconButtonPolicy.setVerticalStretch(0)
        
        # -- przycisk wysłania --        
        self.sendButton = QPushButton(u"&Send", self)
        self.sendButton.setObjectName("sendButton")
        self.sendButton.setIcon(pea_app().send_icon)
        sendSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.sendButton.setSizePolicy(sendSizePolicy)
        self.layout().addWidget(self.sendButton)
        
        self.layout().addStretch()
        
        # -- przycisk dodawania
        self.addButton = QtGui.QPushButton(self)
        self.addButton.setObjectName("addButton")
        self.addButton.setSizePolicy(iconButtonPolicy)
        self.addButton.setIcon(pea_app().add_icon)
        self.layout().addWidget(self.addButton)
        
        # -- przycisk do dat
        self.datesButton = QtGui.QPushButton(self)
        self.datesButton.setCheckable(True)
        self.datesButton.setObjectName("datesButton")
        self.datesButton.setSizePolicy(iconButtonPolicy)
        self.datesButton.setIcon(pea_app().calendar_icon)
        self.layout().addWidget(self.datesButton)
        
        # -- przycisk zamykania
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setSizePolicy(iconButtonPolicy)
        self.closeButton.setIcon(pea_app().close_icon)
        self.layout().addWidget(self.closeButton)
        
class UsersList(QWidget):
    def __init__(self, parent=None):
        super(UsersList, self).__init__(parent)
        self.setLayout(QHBoxLayout(self))
        
    def clearUsers(self):
        layout = self.layout()
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().close()
            layout.takeAt(i)
    
    def addUser(self, username):
        self.layout().addWidget(UserEntry(username))
        
    def setUsers(self, username_list):
        self.clearUsers()
        for uname in username_list:
            self.addUser(uname)
        
    def users(self):
        '''Zwraca listę str wszystkich nazw użytkowników'''
        return [self.layout().itemAt(i).widget().userName() for i in range(self.layout().count())]

      