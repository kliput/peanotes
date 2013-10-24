# -*- coding: utf-8 -*-

import datetime, random
from PySide.QtCore import QObject, Signal

class MsgState():
    NEW = 1
    READED = 2
    TO_SEND = 3
    SENT = 4

class Message():
    def __init__(self, content, recipients, expire_date, state):
        '''
        content - tresc tesktowa
        recipients - lista adresatow i grup adresatow
        expire_date - data waznosci
        state - stan typu MsgState
        '''
        assert isinstance(expire_date, datetime.datetime)
        
        self.content = content
        self.recipients = recipients
        self.expire_date = expire_date
        self.state = state

class MessageBox(object):
    def __init__(self):
        self.__box__ = {}
    def addMsg(self, message):
        'message - typ: Message'
        self.__box__[random.randint(0, 10000)] = message
    def delMsg(self, msgId):
        try:
            del self.__box__[msgId]
        except KeyError:
            print "Tried to remove non-existent message with id: %d" % msgId
    def modMsg(self, msgId, message):
        if not isinstance(message, Message):
            raise TypeError
        try:
            self.__box__[msgId] = message
        except:
            print "Tried to modify non-existent message with id: %d" % msgId
    def getMsgByState(self, state):
        return {mid: msg for (mid, msg) in self.__box__.items() if msg.state == state}
    def getMsgAll(self):
        return self.__box__
    def synchronize(self):
        raise NotImplementedError

class LoginState(object):
    OK = 1
    FAIL = 2

class PeanotesClient(QObject):
    # to sygnał, który po prostu się wywołuje w kodzie "loggedIn.emit(<stan>)"
    # w miejscu, w którym chcemy powiadamiać o poprawnym zalogowaniu się
    loggedIn = Signal(LoginState)    
    
    def __init__(self):
        QObject.__init__(self)
        
        self.msgBox = MessageBox()
        # TESTING CODE ->
        self.msgBox.addMsg(Message("Hello world!",
                                   ['piotrek', 'marek'],
                                   datetime.datetime(2013, 11, 18, 11, 33),
                                   MsgState.NEW))
        self.msgBox.addMsg(Message("Inna wiadomosc",
                                   ['marek', 'kuba'],
                                   datetime.datetime(2014, 10, 18, 11, 33),
                                   MsgState.READED))
        # <- TESTING CODE
            
    def login(self, login, password):
        # logowanie na serwerze...
        # jesli wszystko poszlo dobrze:
        # signal:
        self.signalLoggedIn.emit(LoginState.OK)
