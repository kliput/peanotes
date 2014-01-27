# -*- coding: utf-8 -*-

import os, pickle, sys, datetime, random

from core.message_factory import MsgState, Message, MessageFactory
import uuid

from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *

from gui.notes import SolidNote
from gui.utils import pea_app
from gui.windows import SettingsWindow
from gui.utils import STYLES
from core.filters import FilterQueue

trUtf8 = QObject.trUtf8

class TrayIcon(QSystemTrayIcon):
    def __init__(self, mainGui):
        QSystemTrayIcon.__init__(self)
        
        self.mainGui = mainGui
        
        icon = pea_app().tray_icon
        self.setIcon(icon)
        self.activated.connect(self.handleActivation)
        self.show()
        
        # --- MENU ---
        
        self.menu = QMenu(QApplication.desktop())
        
        # TODO: ikonki dla pozycji w menu
        self.actQuit = QAction(u"&Quit", self.menu)
        self.menu.addAction(self.actQuit)
        self.actQuit.triggered.connect(mainGui.closeApplication)
        
        self.actSettings = QAction(u"&Settings", self.menu)
        self.menu.addAction(self.actSettings)
        self.actSettings.triggered.connect(mainGui.showSettings)

        self.actHideNotes = QAction(u"&Hide notes", self.menu)
        self.menu.addAction(self.actHideNotes)
        self.actHideNotes.triggered.connect(mainGui.hideNotes)
        
        self.actShowNotes = QAction(u"&Show notes", self.menu)
        self.menu.addAction(self.actShowNotes)
        self.actShowNotes.triggered.connect(mainGui.showNotes)
        
        self.actNewNote = QAction(u"&New note", self.menu)
        self.menu.addAction(self.actNewNote)
        self.actNewNote.triggered.connect(mainGui.newNote)
        
        self.setContextMenu(self.menu)
        
    @Slot(QSystemTrayIcon.ActivationReason)
    def handleActivation(self, reason):
        global NOTES
        global NOTE_ID
        
        if reason == QSystemTrayIcon.DoubleClick:
            print "Double"
        
        elif reason == QSystemTrayIcon.Trigger: # lewy przycisk
            self.mainGui.showNotes()
                
#        elif reason == QSystemTrayIcon.Context: # prawy przycisk
#            print 'bye!'
#            sys.exit(0)
#            # TODO: menu
            
        elif reason == QSystemTrayIcon.MiddleClick: # środkowy przycisk
            self.mainGui.newNote()

class LocalSettings(object):
    def __init__(self):
        self.notes = {} # msgId -> note

class MainGui(QObject):
#     SETTINGS_PATH = ".config"
    
    def __init__(self, client):
        self.client = client
        
        self.settingsWindow = SettingsWindow(self)
        self.settingsWindow.hide()
        
        QTextCodec.setCodecForTr(QTextCodec.codecForName("UTF-8"))
        
        # połączenia ->
#         self.client.loggedIn.connect(self.handleLoginState)
        # TODO: dodano notatkę
        # TODO: zmieniono zawartość skrzynki
        # <-
                
#         self.localSettings = self.loadSettings()
#         self.loginWindow = LoginWindow()
#         self.loginWindow.show()
#         
#         self.loginWindow.formSubmitted.connect(self.handleLoginForm)
        
        self.trayIcon = TrayIcon(self)
        
        self.localMessagesIds = []
        self.allNotes = {}
        
        self.handleUpdateMessageBox()
    
        self.client.boxUpdated.connect(self.handleUpdateMessageBox)
                
        # TODO:
        self.__knownUsersSet__ = set(['kuba', 'marek', 'piotrek'])
        
        self.updateNotes()
        
#     @Slot(str, str)
#     def handleLoginForm(self, user, password):
#         self.client.login(user, password)
    
#     @Slot(LoginState)
#     def handleLoginState(self, loginState):
#         if loginState == LoginState.OK:
#             print "logged in successfully!"
#             # TODO: raczej powinno reagować na powiadomienie od klienta
#             self.handleUpdateMessageBox()
#         else:
#             print "login failed!"
    
    def userName(self):
        return self.client.user_name
    
    # TODO:
    def knownUsers(self):
        return list(self.__knownUsersSet__)
    
    def addKnownUser(self, username):
        self.__knownUsersSet__.add(username)
    
    @Slot()
    def handleUpdateMessageBox(self):
        
        # TODO: zmienić na obliczanie różnicy zbiorów
        # NOTICE, WARNING!
#         for note in self.allNotes.values():
#             note.close()

        for mid, msg in self.client.getMsgAll().items():
            if mid not in self.allNotes.keys():
                # utworzenie nowej notatki
                if not msg.state == MsgState.DELETED:
                    self.allNotes[mid] = SolidNote(msg, self)
            else:
                print 'debug: already exists: %s' % str(mid)
                # tylko ew. zmiana stanu
                if msg.state == MsgState.DELETED:
                    print 'state DELETED'
                    self.allNotes[mid].close()
                    del self.allNotes[mid]
                else:
                    self.allNotes[mid].setMessageState(msg.state)
    
        self.updateNotes() # FIXME: ...
    
        for note in self.allNotes.values(): note.show()
    
    @Slot()
    def closeApplication(self):
#        self.saveSettings(self.localSettings) # TODO: settings
        self.client.stopClient()
        QApplication.quit()
        # TODO: ikona w trayu nie znika
        
    @Slot()
    def showSettings(self):
        self.settingsWindow.show()
    
    @Slot()
    def hideNotes(self):
        for note in self.allNotes.values():
            note.hide()
    
    @Slot()
    def showNotes(self):
        for note in self.allNotes.values():
            note.show()
            note.raise_()
            note.activateWindow()
        
        self.updateNotes()

    @Slot()
    def newNote(self):
        # TODO: domyślna data ważności, możliwość zmiany daty ważności
        # do domyslnej daty waznosci mozna wykorzystac MessageFactory, pozniej mozemy podpiac do fabryki wstrzykiwanie domyslnych ustawien
        messageFactory = MessageFactory()
        messageFactory.set_sender(self.userName())
        messageFactory.set_recipients([])
        messageFactory.set_expiredate_policy(MessageFactory.POLICY_EXPIREDATE_DAYS)
        messageFactory.set_days_to_expire(31)
        messageFactory.set_state(MsgState.GUI)
        messageFactory.set_content('')
        
        
        m = messageFactory.build()
        
        nnote = SolidNote(m, self)
        
        self.allNotes[m.msg_uuid] = nnote
        
        # HACK TODO
        self.handleUpdateMessageBox()
        
        # TODO: niepotrzebne, lepiej jakiś refresh
        #self.client.addMsg(m) # TODO: addMsg emituje zmianę zawartości
        
#         self.handleUpdateMessageBox()
    
    def updateNotes(self):
        fq = FilterQueue()
        for f in self.settingsWindow.filters.values():
            fq.add_filter(f[0], f[1]) # FIXME: !
        
        for note in self.allNotes.values():
            try:
                style = STYLES[fq.get_first_matching(note.__message__)]
            except KeyError:
                style = STYLES['yellow']
            note.setStyleSheet(style)
        
#     def loadSettings(self):
#         'TODO: dodać domyślne'        
#         with open(self.SETTINGS_PATH, "rb") as f:
#             try:
#                 s = pickle.load(f)
#             except Exception as e:
#                 print 'settings file not found or corrupted - creating new configuration in %s' % self.SETTINGS_PATH
#                 s = LocalSettings()
#                 self.saveSettings(LocalSettings())
#              
#         return s
        
#     def saveSettings(self, settings):
#         with open(self.SETTINGS_PATH, "wb") as f:
#             pickle.dump(settings, f)
