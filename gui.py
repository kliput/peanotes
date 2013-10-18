#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
from core_mock import *
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
        self.contentLabel = QLabel()
        
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
        self.contentLabel.setText(message.content)
        

class SolidNote(Note):
    def __init__(self, message=None, parent=None):
        super(SolidNote, self).__init__(message, parent)
    
    def paintBackground(self, painter):
        painter.setBrush(QColor('#F8CA00'))
        painter.drawRect(QRectF(0, 0, self.NOTE_WIDTH-1, self.NOTE_HEIGHT-1))
        
class TransculentNote(Note):
    def __init__(self, message=None, parent=None):
        super(TransculentNote, self).__init__(message, parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.BACKGROUND_IMAGE = QImage('back.png') 
    
    def paintBackground(self, painter):
        painter.drawImage(QRectF(0, 0, self.NOTE_WIDTH, self.NOTE_HEIGHT),
                  self.BACKGROUND_IMAGE, QRectF(0, 0, self.NOTE_WIDTH, self.NOTE_HEIGHT))

class LoginWindow(QWidget):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setWindowTitle("Login")
        self.setLayout(QFormLayout())
        
        self.loginEdit = QLineEdit()
        self.passwordEdit = QLineEdit()

        self.layout().addWidget(QLabel('Login:'))
        self.layout().addWidget(self.loginEdit)
        self.layout().addWidget(QLabel('Password:'))
        self.layout().addWidget(self.passwordEdit)

class LocalSettings(object):
    def __init__(self):
        pass

def main_tests():
    
        
    client = Client()
    print client.msgBox.getMsgByState(MsgState.NEW)
    
    app = QApplication(sys.argv)
    
    loginWindow = LoginWindow()
    loginWindow.show()

    allNotes = []
    for _, msg in client.msgBox.getMsgAll().items():
        allNotes.append(SolidNote(msg))
    
    for note in allNotes: note.show()
        
    return app.exec_()
    
#     desktop = QApplication.desktop()
    
#     btn = QPushButton("hello", desktop)
    
#     note1 = Note(desktop)
#     note1.show()
    
#     layout = QFormLayout()
#     layout.addWidget(btn)
#     note1.setLayout(layout)
       
#     note2 = Note(desktop)
#     note2.show()
    
#     note1.setWindowTitle("Hello")
#     note1.setFixedSize(200, 200)
#     note1.show()
    
#     note = QX11Info.isCompositingManagerRunning() and TransculentNote() or SolidNote()


if __name__ == '__main__':
    main_tests()


