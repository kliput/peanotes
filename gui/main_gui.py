# -*- coding: utf-8 -*-

import pickle, sys, datetime

from core.message_factory import MsgState, Message, MessageFactory
import uuid

from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *

import gui # self import for module path

import os
IMAGES_PATH = "%s/images" % os.path.dirname(gui.__file__)

DATETIME_FORMAT = '%d-%m-%Y, %H:%M'

trUtf8 = QObject.trUtf8

def get_image(file_name):
    return "%s/%s" % (IMAGES_PATH, file_name)


class Note(QWidget):
    
    def __init__(self, message, mainGui, parent=None):
        super(Note, self).__init__(parent)
        
        self.mainGui = mainGui
        
        self.NOTE_WIDTH = 240
        self.NOTE_HEIGHT = 240
        
        self.resize(self.NOTE_WIDTH, self.NOTE_HEIGHT)
        
        self.setObjectName("note")
        
        self.drag = False # czy karteczka jest w trakcie przenoszenia?
        self.dragPos = QPoint() # pozycja rozpoczecia przenoszenia
         
        assert message
         
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        
        
        # -- główne layouty --
                
        self.globalVLayout = QtGui.QVBoxLayout(self)
        self.globalVLayout.setObjectName("globalVLayout")
        
        self.upperHLayout = QtGui.QHBoxLayout()
        self.upperHLayout.setObjectName("upperHLayout")
        self.globalVLayout.addLayout(self.upperHLayout)
        
        self.fromToForm = QtGui.QFormLayout()
        self.upperHLayout.addLayout(self.fromToForm)
        
        self.upperButtonsLayout = QtGui.QGridLayout()
        self.upperHLayout.addLayout(self.upperButtonsLayout)
        
        # -- layout z nadawcą i adresatami --
        self.fromToForm.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fromToForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.fromToForm.setObjectName("fromToForm")
        self.fromLabel = QtGui.QLabel("From:", self)
        self.fromLabel.setObjectName("fromLabel")
        self.fromToForm.setWidget(0, QtGui.QFormLayout.LabelRole, self.fromLabel)
        self.fromData = QtGui.QLabel(self)
        self.fromData.setObjectName("fromData")
        self.fromToForm.setWidget(0, QtGui.QFormLayout.FieldRole, self.fromData)
        self.toLabel = QtGui.QLabel("To:", self)
        self.toLabel.setObjectName("toLabel")
        self.fromToForm.setWidget(1, QtGui.QFormLayout.LabelRole, self.toLabel)
        self.toData = QtGui.QLabel(self)
        self.toData.setObjectName("toData")
        self.fromToForm.setWidget(1, QtGui.QFormLayout.FieldRole, self.toData)

        
        # -- przyciski w prawym górnym rogu
        
        # -- przycisk wysłania --        
        self.sendButton = QPushButton(u"&Send", self)
        self.sendButton.setObjectName("sendButton")
        sendIcon = QtGui.QIcon()
        sendIcon.addPixmap(QtGui.QPixmap(get_image("send.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendButton.setIcon(sendIcon)
        self.sendButton.clicked.connect(self.sendMessage)
        sendSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.sendButton.setSizePolicy(sendSizePolicy)
#         self.upperHLayout.addWidget(self.sendButton)
        self.upperButtonsLayout.addWidget(self.sendButton, 0, 0)
        
        # -- przycisk zamykania
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setObjectName("closeButton")
        closeSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        closeSizePolicy.setHorizontalStretch(0)
        closeSizePolicy.setVerticalStretch(0)
        closeSizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        self.closeButton.setSizePolicy(closeSizePolicy)
        closeIcon = QtGui.QIcon()
        closeIcon.addPixmap(QtGui.QPixmap(get_image("close.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(closeIcon)
#         self.upperHLayout.addWidget(self.closeButton)
        self.upperButtonsLayout.addWidget(self.closeButton, 0, 1)
        
        # -- przycisk do dat
        self.datesButton = QtGui.QPushButton(self)
        self.datesButton.setCheckable(True)
        self.datesButton.setObjectName("datesButton")
        closeSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        closeSizePolicy.setHorizontalStretch(0)
        closeSizePolicy.setVerticalStretch(0)
        closeSizePolicy.setHeightForWidth(self.datesButton.sizePolicy().hasHeightForWidth())
        self.datesButton.setSizePolicy(closeSizePolicy)
        closeIcon = QtGui.QIcon()
        closeIcon.addPixmap(QtGui.QPixmap(get_image("calendar.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.datesButton.setIcon(closeIcon)
        self.upperButtonsLayout.addWidget(self.datesButton, 1, 1)

        # -- linia oddzielająca nagłówek od treści
        self.line = QtGui.QFrame(self)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.globalVLayout.addWidget(self.line)

        # -- DATES --

        # TODO: zmniejszyć czcionkę?
        self.datesForm = QtGui.QFormLayout()
        self.datesForm.setObjectName("datesForm")
        self.dateLabel = QtGui.QLabel("Date:", self)
        self.dateLabel.setObjectName("dateLabel")
        self.datesForm.setWidget(0, QtGui.QFormLayout.LabelRole, self.dateLabel)
        self.validLabel = QtGui.QLabel("Valid till:", self)
        self.validLabel.setObjectName("validLabel")
        self.datesForm.setWidget(1, QtGui.QFormLayout.LabelRole, self.validLabel)
        self.dateData = QtGui.QLabel(self)
        self.dateData.setObjectName("dateData")
        self.datesForm.setWidget(0, QtGui.QFormLayout.FieldRole, self.dateData)
        self.validData = QtGui.QLabel(self)
        self.validData.setObjectName("validData")
        self.datesForm.setWidget(1, QtGui.QFormLayout.FieldRole, self.validData)

        self.datesWidget = QtGui.QWidget()
        self.datesWidget.setLayout(self.datesForm)
        self.globalVLayout.addWidget(self.datesWidget)
        
        # -- obsługa chowania dat
        self.datesWidget.hide()
        self.datesButton.toggled.connect(self.toggleDatesWidget)

        
        # -- pole treści
        self.noteContent = QtGui.QTextBrowser(self)
        self.noteContent.setEnabled(True)
        
        self.noteContent.setFrameShape(QtGui.QFrame.NoFrame)
        self.noteContent.setFrameShadow(QtGui.QFrame.Plain)
        self.noteContent.setReadOnly(True)
        self.noteContent.setObjectName("noteContent")
        self.globalVLayout.addWidget(self.noteContent)
        
        
        # -- obsługa zamykania        
        self.closeButton.setShortcut(QtGui.QApplication.translate("Note", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.clicked.connect(self.closeNote)


        # -- ustawienie treści po
        self.setMessage(message)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag = True
            self.dragPos = event.globalPos() - self.pos()
    
    def mouseReleaseEvent(self, event):
        self.drag = False
    
    def mouseMoveEvent(self, event):
        if self.drag:
            self.move(event.globalPos() - self.dragPos)
    
    def updateMessageState(self):
        s = self.__message__.state
        if s == MsgState.GUI:
            self.sendButton.show()
            self.noteContent.setReadOnly(False)
        elif s == MsgState.TO_SEND:
            self.sendButton.show()
            self.sendButton.setDisabled(True)
            self.noteContent.setReadOnly(True)
        elif s == MsgState.DELETED:
            self.close()
        else:
            self.sendButton.hide()
            self.noteContent.setReadOnly(True)
    
    def setMessageState(self, state):
        self.__message__.state = state
        self.updateMessageState()
    
    def setMessage(self, message):
        assert message
        self.__message__ = message
        
        # TODO: dodać trzykropek jak się nie mieści
        self.fromData.setText(message.sender)
        self.toData.setText(', '.join(message.recipients))
        # TODO: przyciąć daty do minut
        self.dateData.setText(message.create_date.strftime(DATETIME_FORMAT))
        self.validData.setText(message.expire_date.strftime(DATETIME_FORMAT))
        self.noteContent.setHtml(message.content)
        
        self.updateMessageState()
    
    def sendMessage(self):
        # tylko dla całkiem nowych wiadomości (w sumie tylko powinny być)
        if self.__message__.state == MsgState.GUI:
            self.__message__.content = self.noteContent.toPlainText()
            self.setMessageState(MsgState.TO_SEND)
        self.mainGui.client.addMsg(self.__message__)
    
    def getMessage(self):
        return self.__message__
    
    @Slot()
    def closeNote(self):
        '''dla przycisku zamykania - tylko ustawia stan
        reszta jest obsługiwana przez zmianę stanu'''
        self.setMessageState(MsgState.DELETED)
        # TODO: do tego można zrobić inną metodę przesyłającą tylko nowy stan...
        self.mainGui.client.modMsg(self.__message__)
    
    @Slot()
    def toggleDatesWidget(self, visibility):
        '''dla widgetu z datami - przełączanie widoczności'''
        if visibility:
            self.datesWidget.show()
        else:
            self.datesWidget.hide()

class SolidNote(Note):
    def __init__(self, message=None, parent=None):
        super(SolidNote, self).__init__(message, parent)
        self.setStyleSheet('''
        QWidget#note {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                stop:0 rgba(249, 247, 105, 255), stop:1 rgba(232, 202, 33, 255));
        }
        
        QPushButton {
            padding: 4px;
            border-style: solid;
            background-color: rgba(255, 255, 255, 80);
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 120);
        }
        
        QPushButton:pressed {
            background-color: rgba(0, 0, 0, 120);
        }
        
        QPushButton:checked {
            background-color: rgba(0, 0, 0, 80);
        }
        
        QTextBrowser#noteContent {
            background-color: rgba(255, 255, 255, 80);
        }
        ''')
        # TODO: zmiana kolorów
            
#     def paintBackground(self, painter):
#         painter.setBrush(QColor('#F8CA00')) # TODO: konfiguracja koloru
#         painter.drawRect(QRectF(0, 0, self.NOTE_WIDTH-1, self.NOTE_HEIGHT-1))
        
# class TransculentNote(Note):
#     'not done yet'
#     def __init__(self, message=None, parent=None):
#         super(TransculentNote, self).__init__(message, parent)
#         self.setAttribute(Qt.WA_TranslucentBackground)
#         self.BACKGROUND_IMAGE = QImage('back.png') 
#     
#     def paintBackground(self, painter):
#         painter.drawImage(QRectF(0, 0, self.NOTE_WIDTH, self.NOTE_HEIGHT),
#                   self.BACKGROUND_IMAGE, QRectF(0, 0, self.NOTE_WIDTH, self.NOTE_HEIGHT))

# class LoginWindow(QWidget):
#     # naciśnięcie OK - wysłanie danych logowania
#     formSubmitted = Signal((str, str))
#     
#     def __init__(self, mainGui, parent=None):
#         super(LoginWindow, self).__init__(parent)
#         
#         self.mainGui = mainGui
#         
#         self.setWindowTitle("Login")
#         self.setLayout(QFormLayout())
#         
#         self.loginEdit = QLineEdit()
#         self.passwordEdit = QLineEdit()
#         self.submitButton = QPushButton('OK')
#         self.cancelButton = QPushButton('Cancel')
# 
#         self.submitButton.clicked.connect(self.handleOKButton())
# 
#         self.layout().addRow('Login:', self.loginEdit)
#         self.layout().addRow('Password:', self.passwordEdit)
#         self.buttonsLayout = QHBoxLayout()
#         self.buttonsLayout.addWidget(self.submitButton)
#         self.buttonsLayout.addWidget(self.cancelButton)
#         self.layout().addLayout(self.buttonsLayout)
# 
#     @Slot
#     def handleOKButton(self):
#         self.formSubmitted.emit(self.loginEdit.text(), self.passwordEdit.text())
#         # TODO: efekt ładowania - oczekiwanie na odpowiedź mainGui

class TrayIcon(QSystemTrayIcon):
    def __init__(self, mainGui):
        QSystemTrayIcon.__init__(self)
        
        self.mainGui = mainGui
        
        icon = QIcon(get_image('icon.png'))
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
    
        # TODO: nazwa użytkownika
        self.userName = client.jid.split('@')[0]
        print 'username: %s' % self.userName
    
        self.client.boxUpdated.connect(self.handleUpdateMessageBox)
        
    
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
    
        for note in self.allNotes.values(): note.show()
    
    @Slot()
    def closeApplication(self):
#        self.saveSettings(self.localSettings) # TODO: settings
        self.client.stopClient()
        QApplication.quit()
        # TODO: ikona w trayu nie znika
        
    @Slot()
    def showSettings(self):
        # TODO: settings window
        pass
    
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

    @Slot()
    def newNote(self):
        # TODO: domyślna data ważności, możliwość zmiany daty ważności
        # do domyslnej daty waznosci mozna wykorzystac MessageFactory, pozniej mozemy podpiac do fabryki wstrzykiwanie domyslnych ustawien
        messageFactory = MessageFactory()
        messageFactory.set_sender(self.userName)
        messageFactory.set_recipients(['kowalski'])
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
