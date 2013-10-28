# -*- coding: utf-8 -*-

from PySide.QtCore import QObject, Signal
from message_factory import MessageFactory
from message_factory import MsgState
from message_factory import Message

from client_agent import ClientAgent

class MessageBox(object):
    def __init__(self):
        self.__box__ = {}
    def addMsg(self, message):
        'message - typ: Message'
        self.__box__[message.msg_uuid] = message
    def delMsg(self, message):
        try:
            del self.__box__[message.msg_uuid]
        except KeyError:
            print "Tried to remove non-existent message with id: %d" % message.msg_uuid
    def modMsg(self, message):
        if not isinstance(message, Message):
            raise TypeError
        try:
            self.__box__[message.msg_uuid] = message
        except:
            print "Tried to modify non-existent message with id: %d" % message.msg_uuid
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
    boxUpdated = Signal()
    
    def __init__(self, jid, password):
        QObject.__init__(self)
        
        self.agent = ClientAgent(jid, password, self)
        self.agent.start()
        
        self.jid = jid
        self.password = password
        
        self.__box__ = {}
        # TESTING CODE ->
        c1 = u'''Maecenas sed interdum dolor, eu elementum mi. Proin feugiat pulvinar mi, id feugiat metus scelerisque et. Praesent scelerisque tellus a libero laoreet, varius consectetur felis iaculis. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Nam justo dolor, vestibulum et adipiscing ut, pulvinar id risus. Etiam metus lorem, auctor at placerat ac, luctus et magna. Sed bibendum laoreet nulla. 
Fusce vulputate, ligula ac cursus lacinia, magna quam feugiat tellus, nec elementum metus est ac diam. Curabitur erat ipsum, egestas eu sem quis, gravida blandit nulla. Fusce vel mi facilisis, mollis tortor id, dignissim metus. Integer iaculis dignissim eleifend. Curabitur condimentum euismod augue, a scelerisque nisi fermentum sit amet. Donec scelerisque ultricies mi nec elementum. Curabitur sagittis urna ac tincidunt ultrices. Praesent lobortis dolor ut arcu vestibulum adipiscing. Phasellus eget congue purus. In non scelerisque mi. Donec in tortor scelerisque, fringilla lectus id, ullamcorper erat. Phasellus eget tempor tellus. Donec vitae convallis enim.'''
        factory = MessageFactory()
        factory.set_sender('piotrek')
        
        factory.set_content(c1)
        factory.set_recipients(['piotrek', 'marek'])
        self.addMsg(factory.build())
        factory.set_content(u'Inna wiadomość')
        factory.set_recipients(['piotrek', 'marek'])
        self.addMsg(factory.build())
#        self.msgBox.addMsg(Message(c1, 'kuba',
#                                   ['piotrek', 'marek'],
#                                   datetime.datetime.today(),
#                                   datetime.datetime(2013, 11, 18, 11, 33),
#                                   MsgState.NEW))
#        self.msgBox.addMsg(Message(u'Inna wiadomość', 'piotrek',
#                                   ['marek', 'kuba'],
#                                   datetime.datetime.today(),
#                                   datetime.datetime(2014, 10, 18, 11, 33),
#                                   MsgState.READED))
        # <- TESTING CODE
            
    def login(self, login, password):
        print login, password
        # logowanie na serwerze...
        # jesli wszystko poszlo dobrze:
        # signal:
        self.signalLoggedIn.emit(LoginState.OK)

    def addMsg(self, message):
        'message - typ: Message'
        self.agent.sendMsg(message)
        import behaviours
        self.agent.runBehaviourOnce(behaviours.SyncRequestBehaviour())
#         self.__box__[message.msg_uuid] = message
#     def delMsg(self, message):
#         try:
#             del self.__box__[message.msg_uuid]
#         except KeyError:
#             print "Tried to remove non-existent message with id: %d" % message.msg_uuid
#     def modMsg(self, message):
#         if not isinstance(message, Message):
#             raise TypeError
#         try:
#             self.__box__[message.msg_uuid] = message
#         except:
#             print "Tried to modify non-existent message with id: %d" % message.msg_uuid
#     def getMsgByState(self, state):
#         return {mid: msg for (mid, msg) in self.__box__.items() if msg.state == state}
    def getMsgAll(self):
        return self.__box__
    
    def agentUpdated(self, messages):
        print 'agent updated: %s' % messages
        for m in messages:
            self.__box__[m.msg_uuid] = m
        
        # TODO: przesyłanie nowych do gui 
        self.boxUpdated.emit()
