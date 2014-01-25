# -*- coding: utf-8 -*-

from PySide.QtGui import QWidget 
from PySide.QtCore import Slot, Qt
from gui.ui.add_user_window import Ui_AddUserWindow
from gui.ui.settings_window import Ui_PeanotesSettings
from gui.utils import list_widget_items, pea_app
from core.filters import AndFilter, RecepientFilter, SenderFilter, RegexFilter,\
    WordFilter
    
from gui.utils import STYLES
 
class SelectRecipientsWindow(QWidget):
    def __init__(self, note):
        '''
        Argument parent powinien być notatką (typ Note)
        '''
        super(SelectRecipientsWindow, self).__init__(None)
        self.ui = Ui_AddUserWindow()
        self.ui.setupUi(self)
        self.note = note
        self.setWindowIcon(pea_app().add_icon)
    
    def init(self):
        kusers = set(self.note.knownUsers())
        rusers = set(self.note.recipients())
        
        self.ui.knownUsersList.clear()
        self.ui.recipientsList.clear()
        
        self.ui.knownUsersList.addItems(list(kusers-(kusers & rusers)))
        self.ui.recipientsList.addItems(list(rusers))
        
        self.ui.doneButton.clicked.connect(self.doneClicked)
        
        self.ui.addButton.clicked.connect(self.addSelectedUsers)
        self.ui.addAllButton.clicked.connect(self.addAllUsers)
        self.ui.removeButton.clicked.connect(self.removeSelectedRecipients)
        self.ui.removeAllButton.clicked.connect(self.removeAllRecipients)
    
        self.ui.addUnknownButton.clicked.connect(self.addUnknownUser)
        self.ui.unknownUserEdit.returnPressed.connect(self.addUnknownUser)
    
    def showEvent(self, event):
        self.init()
    
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
    
    @Slot() 
    def addUnknownUser(self):
        uu = self.ui.unknownUserEdit.text()
        if uu and uu != '':
            rlist = self.ui.recipientsList
            if uu not in [it.text() for it in list_widget_items(rlist)]:
                rlist.addItem(uu)
            self.ui.unknownUserEdit.clear()
            self.note.addKnownUser(uu)
 
class SettingsWindow(QWidget):    
    def __init__(self, mainGui):
        '''
        Argument parent powinien być typu MainGui
        '''
        super(SettingsWindow, self).__init__(None)
        self.ui = Ui_PeanotesSettings()
        self.ui.setupUi(self)
        self.mainGui = mainGui
        self.setWindowIcon(pea_app().tray_icon)
    
        self.filters = {}
        self.iter = 1
        
        self.ui.addButton.clicked.connect(self.addFilter)
        self.ui.removeButton.clicked.connect(self.removeFilter)
        
        self.ui.saveButton.clicked.connect(self.updateFilter)
        
        self.ui.colorBox.addItems(STYLES.keys())
    
    def init(self):
        pass
    
    @Slot()
    def addFilter(self):
        name = 'Filter #%d' % self.iter
        self.iter += 1
        
        self.filters[name] = (AndFilter([]), 'yellow') # pusty - matchuje wszystko
        self.ui.filtersList.addItem(name)
    
    @Slot()
    def updateFilter(self):
        item_key = self.ui.filtersList.selectedItems()[0].text()
        
        # budowa nowego filtra
        sender = self.ui.fromEdit.text()
        recipient = self.ui.toEdit.text()
        content = self.ui.containsEdit.toPlainText()
        
        tmp_fs = []
        
        if sender:
            tmp_fs.append(SenderFilter(sender))
        if recipient:
            tmp_fs.append(RecepientFilter(recipient))
        if content:
            tmp_fs.append(WordFilter(content))
                
        self.filters[item_key] = (AndFilter(tmp_fs), self.ui.colorBox.currentText())
        
        self.mainGui.updateNotes()
    
    @Slot()
    def removeFilter(self):
        for item in self.ui.filtersList.selectedItems():
            self.ui.filtersList.takeItem(self.ui.filtersList.row(item))
    
    def hideEvent(self, *args, **kwargs):
        self.mainGui.updateNotes()
        