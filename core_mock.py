# -*- coding: utf-8 -*-

import datetime, random
from PySide.QtCore import QObject, Signal

class MsgState():
    NEW = 1
    READED = 2
    TO_SEND = 3
    SENT = 4

class Message():
    def __init__(self, content, sender, recipients, create_date, expire_date, state):
        '''
        content - tresc tesktowa
        recipients - lista adresatow i grup adresatow
        expire_date - data waznosci
        state - stan typu MsgState
        '''
        assert isinstance(expire_date, datetime.datetime)
        
        self.content = content
        self.sender = sender
        self.recipients = recipients
        self.create_date = create_date
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
        c1 = u'''Maecenas sed interdum dolor, eu elementum mi. Proin feugiat pulvinar mi, id feugiat metus scelerisque et. Praesent scelerisque tellus a libero laoreet, varius consectetur felis iaculis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nam justo dolor, vestibulum et adipiscing ut, pulvinar id risus. Etiam metus lorem, auctor at placerat ac, luctus et magna. Sed bibendum laoreet nulla. 
Fusce vulputate, ligula ac cursus lacinia, magna quam feugiat tellus, nec elementum metus est ac diam. Curabitur erat ipsum, egestas eu sem quis, gravida blandit nulla. Fusce vel mi facilisis, mollis tortor id, dignissim metus. Integer iaculis dignissim eleifend. Curabitur condimentum euismod augue, a scelerisque nisi fermentum sit amet. Donec scelerisque ultricies mi nec elementum. Curabitur sagittis urna ac tincidunt ultrices. Praesent lobortis dolor ut arcu vestibulum adipiscing. Phasellus eget congue purus. In non scelerisque mi. Donec in tortor scelerisque, fringilla lectus id, ullamcorper erat. Phasellus eget tempor tellus. Donec vitae convallis enim.'''
        
        self.msgBox.addMsg(Message(c1, 'kuba',
                                   ['piotrek', 'marek'],
                                   datetime.datetime.today(),
                                   datetime.datetime(2013, 11, 18, 11, 33),
                                   MsgState.NEW))
        self.msgBox.addMsg(Message(u'Inna wiadomość', 'piotrek',
                                   ['marek', 'kuba'],
                                   datetime.datetime.today(),
                                   datetime.datetime(2014, 10, 18, 11, 33),
                                   MsgState.READED))
        # <- TESTING CODE
            
    def login(self, login, password):
        # logowanie na serwerze...
        # jesli wszystko poszlo dobrze:
        # signal:
        self.signalLoggedIn.emit(LoginState.OK)
