# -*- coding: utf-8 -*-

from PySide.QtCore import QObject, Signal
from message_factory import MessageFactory
from message_factory import MsgState
from message_factory import Message

from agents import behaviours

from agents.client_agent import ClientAgent

import re

RE_JID = re.compile(r'(.*)@(.*)')

def inner_name(jid):
    '''Przetwórz JID na nazwę użytkownika'''
    return RE_JID.match(jid).group(1)

class LoginState(object):
    OK = 1
    FAIL = 2

class PeanotesClient(QObject):
    # to sygnał, który po prostu się wywołuje w kodzie "loggedIn.emit(<stan>)"
    # w miejscu, w którym chcemy powiadamiać o poprawnym zalogowaniu się
    loggedIn = Signal(LoginState)
    boxUpdated = Signal()
    
    def __init__(self, jid, password):
        QObject.__init__(self)
        
        self.agent = ClientAgent(jid, password, self)
        self.agent.start()
        
        self.jid = jid
        self.password = password
        
        self.user_name = inner_name(self.jid)
        
        self.__box__ = {}
            
    def login(self, login, password):
        print login, password
        # logowanie na serwerze...
        # jesli wszystko poszlo dobrze:
        # signal:
        self.signalLoggedIn.emit(LoginState.OK)

    def addMsg(self, message):
        'message - typ: Message'
        message.state = MsgState.TO_SEND
        self.agent.sendMsg(message)
        self.agent.runBehaviourOnce(behaviours.SyncRequestBehaviour())
        
    def modMsg(self, message):
        self.agent.updateMsg(message)
        self.agent.runBehaviourOnce(behaviours.SyncRequestBehaviour())

    def getMsgAll(self):
        return self.__box__
    
    def agentUpdated(self, messages):
        print 'agent updated: %s' % messages
        for m in messages:
            self.__box__[m.msg_uuid] = m
        self.boxUpdated.emit()
        
    def stopClient(self):
        self.agent.stop()
