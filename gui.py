# -*- coding: utf-8 -*-

import pickle, sys
from core_mock import PeanotesClient, LoginState
from PySide.QtCore import *
from PySide.QtGui import *

class Note(QWidget):
    def __init__(self, message, parent=None):
        super(Note, self).__init__(parent)
        
        self.NOTE_WIDTH = 200
        self.NOTE_HEIGHT = 230
        
        self.drag = False # czy karteczka jest w trakcie przenoszenia?
        self.dragPos = QPoint() # pozycja rozpoczecia przenoszenia
        
        assert message
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(self.NOTE_WIDTH, self.NOTE_HEIGHT)
        self.setLayout(QGridLayout())
        
        self.dateLabel = QLabel()
        self.recipientsLabel = QLabel()
#         self.contentLabel = QLabel() # TODO: ma być pasek przewijania
        self.contentLabel = QPlainTextEdit()
        
        self.layout().addWidget(self.dateLabel)
        self.layout().addWidget(self.recipientsLabel)
        self.layout().addWidget(self.contentLabel)
        
        self.setMessage(message)
                
    def paintEvent(self, *args, **kwargs):
        painter = QPainter(self)
        self.paintBackground(painter)
        pass
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag = True
            self.dragPos = event.globalPos() - self.pos()
    
    def mouseReleaseEvent(self, event):
        self.drag = False
    
    def mouseMoveEvent(self, event):
        if self.drag:
            self.move(event.globalPos() - self.dragPos)
    
    def setMessage(self, message):
        assert message
        self.__message__ = message
        self.dateLabel.setText(str(message.expire_date))
        self.recipientsLabel.setText(', '.join(message.recipients))
        self.contentLabel.setPlainText(message.content)
    
    def getMessage(self):
        return self.__message__

class SolidNote(Note):
    def __init__(self, message=None, parent=None):
        super(SolidNote, self).__init__(message, parent)
    
    def paintBackground(self, painter):
        painter.setBrush(QColor('#F8CA00')) # TODO: konfiguracja koloru
        painter.drawRect(QRectF(0, 0, self.NOTE_WIDTH-1, self.NOTE_HEIGHT-1))
        
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

class LocalSettings(object):
    def __init__(self):
        self.notes = {} # msgId -> note

class MainGui(QObject):
#     SETTINGS_PATH = ".config"
    
    def __init__(self, client):
        self.client = client
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
        
        self.allNotes = []
        
        self.handleUpdateMessageBox()
    
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
        for _, msg in self.client.msgBox.getMsgAll().items():
            self.allNotes.append(SolidNote(msg))
    
        for note in self.allNotes: note.show()
    
    @Slot()
    def handleCloseApplication(self):
        self.saveSettings(self.localSettings)
        
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
