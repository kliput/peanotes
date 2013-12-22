# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget 
from PySide.QtCore import Slot, Qt
from gui.ui.add_user_window import Ui_AddUserWindow
from gui.utils import list_widget_items
 
class SelectRecipientsWindow(QWidget):
    def __init__(self, note):
        '''
        Argument parent powinien być notatką (typ Note)
        '''
        super(SelectRecipientsWindow, self).__init__(None)
        self.ui = Ui_AddUserWindow()
        self.ui.setupUi(self)
        
        self.note = note
        
        self.ui.knownUsersList.addItems(self.note.knownUsers())
        self.ui.recipientsList.addItems(self.note.recipients())
        
        self.ui.doneButton.clicked.connect(self.doneClicked)
        
        self.ui.addButton.clicked.connect(self.addSelectedUsers)
        self.ui.addAllButton.clicked.connect(self.addAllUsers)
        self.ui.removeButton.clicked.connect(self.removeSelectedRecipients)
        self.ui.removeAllButton.clicked.connect(self.removeAllRecipients)
    
    
    def recipients(self):
        return [it.text() for it in list_widget_items(self.ui.recipientsList)]
    
    @Slot()
    def doneClicked(self):
        self.note.setRecipients(self.recipients())
        self.close()
    
    # TODO: do poniższych można zrobić uogólnione metody
    
    @Slot()
    def addSelectedUsers(self):
        klist = self.ui.knownUsersList
        rlist = self.ui.recipientsList
        itemsToMove = [it for it in klist.selectedItems()]
        rlist.addItems([it.text() for it in itemsToMove])
        for item in itemsToMove:
            klist.takeItem(klist.row(item))
    
    @Slot()
    def addAllUsers(self):
        klist = self.ui.knownUsersList
        rlist = self.ui.recipientsList
        rlist.addItems([it.text() for it in list_widget_items(klist)])
        klist.clear()

    @Slot()
    def removeAllRecipients(self):
        klist = self.ui.knownUsersList
        rlist = self.ui.recipientsList
        klist.addItems([it.text() for it in list_widget_items(rlist)])
        rlist.clear()

    @Slot()
    def removeSelectedRecipients(self):
        klist = self.ui.knownUsersList
        rlist = self.ui.recipientsList
        itemsToMove = [it for it in rlist.selectedItems()]
        klist.addItems([it.text() for it in itemsToMove])
        for item in itemsToMove:
            rlist.takeItem(rlist.row(item))
        