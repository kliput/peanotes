# -*- coding: utf-8 -*-

import pickle, sys
from core_mock import PeanotesClient, LoginState
from PySide import QtGui
from PySide import QtCore
from PySide.QtCore import *
from PySide.QtGui import *

class Note(QWidget):
    def __init__(self, message, parent=None):
        super(Note, self).__init__(parent)
        
        self.NOTE_WIDTH = 240
        self.NOTE_HEIGHT = 240
        
        self.resize(self.NOTE_WIDTH, self.NOTE_HEIGHT)
        
        self.setObjectName("Note")
        
        self.drag = False # czy karteczka jest w trakcie przenoszenia?
        self.dragPos = QPoint() # pozycja rozpoczecia przenoszenia
         
        assert message
         
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        
        # ---
        
        self.globalVLayout = QtGui.QVBoxLayout(self)
        self.globalVLayout.setObjectName("globalVLayout")
        
        self.upperHLayout = QtGui.QHBoxLayout()
        self.upperHLayout.setObjectName("upperHLayout")
        
        self.fromToForm = QtGui.QFormLayout()
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
        self.upperHLayout.addLayout(self.fromToForm)
        
        self.closeButton = QtGui.QPushButton(self)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.closeButton.sizePolicy().hasHeightForWidth())
        
        self.closeButton.setSizePolicy(sizePolicy)
        # TODO: usunąć bevel przy najechaniu i naciskaniu
        self.closeButton.setStyleSheet('''QPushButton#closeButton { 
            border-width: 0px;
            min-width: 16px;
            max-width: 16px;
            min-height: 16px;
            max-height: 16px; };''')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon)
        self.closeButton.setFlat(True)
        self.closeButton.setObjectName("closeButton")
        self.upperHLayout.addWidget(self.closeButton)
        self.globalVLayout.addLayout(self.upperHLayout)

        self.line = QtGui.QFrame(self)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName("line")
        self.globalVLayout.addWidget(self.line)

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
        self.globalVLayout.addLayout(self.datesForm)


        self.noteContent = QtGui.QTextBrowser(self)
        self.noteContent.setEnabled(True)
        self.noteContent.setStyleSheet('''QTextBrowser#noteContent {
        background-color: rgba(255, 255, 255, 80); };''')
        
        self.noteContent.setFrameShape(QtGui.QFrame.NoFrame)
        self.noteContent.setFrameShadow(QtGui.QFrame.Plain)
        self.noteContent.setReadOnly(True)
        self.noteContent.setObjectName("noteContent")
        self.globalVLayout.addWidget(self.noteContent)
        
        # ---
        
        self.closeButton.setShortcut(QtGui.QApplication.translate("Note", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.noteContent.setHtml(QtGui.QApplication.translate("Note", "Hello world.", None, QtGui.QApplication.UnicodeUTF8))
#         
        self.setMessage(message)
                
#     def paintEvent(self, *args, **kwargs):
#         painter = QPainter(self)
# #         self.paintBackground(painter)
    
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
        
        # TODO: dodać trzykropek jak się nie mieści
        self.fromData.setText(message.sender)
        self.toData.setText(', '.join(message.recipients))
        # TODO: przyciąć daty do minut
        self.dateData.setText(str(message.create_date))
        self.validData.setText(str(message.expire_date))
        self.noteContent.setHtml(message.content)
    
    def getMessage(self):
        return self.__message__

class SolidNote(Note):
    def __init__(self, message=None, parent=None):
        super(SolidNote, self).__init__(message, parent)
        self.setStyleSheet('''QWidget#Note {
        background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
            stop:0 rgba(249, 247, 105, 255), stop:1 rgba(232, 202, 33, 255));
        };''')
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
