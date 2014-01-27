# -*- coding: utf-8 -*-

from PySide import QtGui
from PySide.QtGui import QWidget, QPushButton, QLabel
from PySide.QtCore import QPoint, Qt, Slot, Signal

from core.message_factory import MsgState
from gui.widgets import UserEntry, ToolBar, UsersList
from gui.utils import STYLES
from gui.windows import SelectRecipientsWindow

from gui.utils import pea_app, trunc_str

DATETIME_FORMAT = '%d-%m-%Y, %H:%M'
USERS_LIST_WIDTH = 200

class Note(QtGui.QWidget):
    
    def __init__(self, message, mainGui, parent=None):
        super(Note, self).__init__(parent)
        
        self.mainGui = mainGui
        
        self.NOTE_WIDTH = 240
        self.NOTE_HEIGHT = 240
        
        self.setFixedSize(self.NOTE_WIDTH, self.NOTE_HEIGHT)
        
        self.setObjectName("note")
        
        self.drag = False # czy karteczka jest w trakcie przenoszenia?
        self.dragPos = QPoint() # pozycja rozpoczecia przenoszenia
        
        assert message
         
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("Note") # FIXME
        
        
        # -- główne layouty --
                
        self.globalVLayout = QtGui.QVBoxLayout(self)
        self.globalVLayout.setObjectName("globalVLayout")
                
        self.upperHLayout = QtGui.QHBoxLayout()
        self.upperHLayout.setObjectName("upperHLayout")
        self.globalVLayout.addLayout(self.upperHLayout)
        
        self.fromToForm = QtGui.QFormLayout()
        self.upperHLayout.addLayout(self.fromToForm)
        
        # -- layout z nadawcą i adresatami --
        self.fromToForm.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.fromToForm.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.fromToForm.setObjectName("fromToForm")
        
        self.fromLabel = QtGui.QLabel("From:", self)
        self.fromLabel.setObjectName("fromLabel")
        self.fromToForm.setWidget(0, QtGui.QFormLayout.LabelRole, self.fromLabel)
        
        self.fromToFormUpRight = QtGui.QHBoxLayout()
        self.fromToForm.setLayout(0, QtGui.QFormLayout.FieldRole, self.fromToFormUpRight)
        
        self.toLabel = QtGui.QLabel("To:", self)
        self.toLabel.setObjectName("toLabel")
        self.fromToForm.setWidget(1, QtGui.QFormLayout.LabelRole, self.toLabel)
        
        self.fromToFormDownRight = QtGui.QHBoxLayout()
        self.fromToForm.setLayout(1, QtGui.QFormLayout.FieldRole, self.fromToFormDownRight)
        
        
        # -- przyciski funkcyjne --        
        iconButtonPolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        iconButtonPolicy.setHorizontalStretch(0)
        iconButtonPolicy.setVerticalStretch(0)
                
        # -- przycisk wysłania --        
        self.sendButton = QPushButton(u"&Send")
        self.sendButton.setObjectName("sendButton")
        self.sendButton.setIcon(pea_app().send_icon)
        sendSizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.sendButton.setSizePolicy(sendSizePolicy)
        
        # -- przycisk dodawania
        self.addButton = QtGui.QPushButton(self)
        self.addButton.setObjectName("addButton")
        self.addButton.setSizePolicy(iconButtonPolicy)
        self.addButton.setIcon(pea_app().add_icon)
        
        self.sendButton.clicked.connect(self.sendMessage)
        
        # -- przycisk do dat
        self.datesButton = QtGui.QPushButton(self)
        self.datesButton.setCheckable(True)
        self.datesButton.setObjectName("datesButton")
        self.datesButton.setSizePolicy(iconButtonPolicy)
        self.datesButton.setIcon(pea_app().calendar_icon)
        
        # -- przycisk zamykania
        self.closeButton = QtGui.QPushButton(self)
        self.closeButton.setObjectName("closeButton")
        self.closeButton.setSizePolicy(iconButtonPolicy)
        self.closeButton.setIcon(pea_app().close_icon)
        
        
        
        # --- górny prawy ---
        self.senderUserEntry = QtGui.QLabel('')
        self.senderUserEntry.setObjectName("senderUserEntry")
        self.fromToFormUpRight.addWidget(self.senderUserEntry)
        self.fromToFormUpRight.addStretch()
        self.fromToFormUpRight.addWidget(self.sendButton)
        self.fromToFormUpRight.addWidget(self.datesButton)
        self.fromToFormUpRight.addWidget(self.closeButton)
        # ---

        # --- dolny prawy ---
        self.recipientsBox = QtGui.QLabel()
        self.fromToFormDownRight.addWidget(self.recipientsBox)
        self.fromToFormDownRight.addStretch()
        self.fromToFormDownRight.addWidget(self.addButton)
        # ---
        

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
        
        # TODO:
        # -- obsługa dodawania adresata
        self.addButton.clicked.connect(self.selectRecipients)

        
        # -- pole treści
        self.noteContent = QtGui.QTextBrowser(self)
        self.noteContent.setEnabled(True)
        
        self.noteContent.setFrameShape(QtGui.QFrame.NoFrame)
        self.noteContent.setFrameShadow(QtGui.QFrame.Plain)
        self.noteContent.setReadOnly(True)
        self.noteContent.setObjectName("noteContent")
        self.globalVLayout.addWidget(self.noteContent)
        
        
        # -- obsługa zamykania        
        self.closeButton.setShortcut(QtGui.QApplication.translate("note", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.clicked.connect(self.closeNote)

        # -- przyszłe okno wyboru adresatów 
        self.selectRecipentsWindow = None

        # -- ustawienie treści
        self.setMessage(message)
    
    
    def setRecipients(self, recipients):
        '''Ustawia listę nadawców
        Argument recipients: lista str [odbiorca1, odbiorca2, ...]'''
        self.recipients_ = recipients
                
        rec_join = ', '.join(recipients)
        self.recipientsBox.setText(trunc_str(rec_join, 21))
        self.recipientsBox.setToolTip(rec_join)
    
    def setSender(self, sender):
        '''Ustawia wysyłającego
        Argument sender: str nadawca'''
        self.sender_ = sender
    
    def mousePressEvent(self, event):
        self.raise_()
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
        send_button = False
        if s == MsgState.GUI:
            self.noteContent.setReadOnly(False)
            send_button = True
            self.addButton.show()
        elif s == MsgState.TO_SEND:
            send_button = True
            self.addButton.setDisabled(True)
            self.sendButton.setDisabled(True)
            self.noteContent.setReadOnly(True)
        elif s == MsgState.DELETED:
            self.close()
        else:
            self.sendButton.hide()
            self.addButton.hide()
            self.noteContent.setReadOnly(True)
            
        if send_button:
            self.sendButton.show()
            self.senderUserEntry.setText(trunc_str(self.sender(), 6))
        else:
            self.senderUserEntry.setText(trunc_str(self.sender(), 16))
            
        self.senderUserEntry.setToolTip(self.sender())
    
    def setMessageState(self, state):
        self.__message__.state = state
        self.updateMessageState()
    
    def setMessage(self, message):
        assert message
        self.__message__ = message
        
        self.setSender(message.sender)
        self.setRecipients(message.recipients)
        self.dateData.setText(message.create_date.strftime(DATETIME_FORMAT))
        self.validData.setText(message.expire_date.strftime(DATETIME_FORMAT))
        self.noteContent.setHtml(message.content)
        
        self.updateMessageState()
    
    def sendMessage(self):
        # tylko dla całkiem nowych wiadomości (w sumie tylko powinny być)
        if self.__message__.state == MsgState.GUI:
            self.__message__.content = self.noteContent.toPlainText()
            self.__message__.sender = self.sender()
            self.__message__.recipients = self.recipients()
            self.setMessageState(MsgState.TO_SEND)
        self.mainGui.client.addMsg(self.__message__)
        self.mainGui.updateNotes()
    
    def getMessage(self):
        return self.__message__
    
    def sender(self):
        return self.sender_
    
    def recipients(self):
        '''Zwraca listę str adresatów'''
        return self.recipients_
    
    def knownUsers(self):
        '''Zwraca listę znanych użytkowników'''
        return self.mainGui.knownUsers()
    
    def addKnownUser(self, username):
        self.mainGui.addKnownUser(username)
    
    @Slot()
    def closeNote(self):
        '''Dla przycisku zamykania - tylko ustawia stan DELETED.
        Reszta działań jest obsługiwana przez zmianę stanu'''
        self.setMessageState(MsgState.DELETED)
        # TODO: do tego można zrobić inną metodę przesyłającą tylko nowy stan...
        self.mainGui.client.modMsg(self.__message__)
    
    @Slot()
    def toggleDatesWidget(self, visibility):
        '''Dla widgetu z datami - przełączanie widoczności'''
        if visibility:
            self.datesWidget.show()
        else:
            self.datesWidget.hide()
            
    @Slot()
    def selectRecipients(self):
        if not self.selectRecipentsWindow:
            self.selectRecipentsWindow = SelectRecipientsWindow(self)
        self.selectRecipentsWindow.show()
    

class SolidNote(Note):
    def __init__(self, message=None, parent=None):
        super(SolidNote, self).__init__(message, parent)
        
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
