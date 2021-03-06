#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import spade
from core import serializer
from behaviours import *
from core.persistence import MessageManager
from agents import groups
class ServerAgent(spade.Agent.Agent):
    
 
#    currently this behaviour is not needed
    class UserOfflineBehaviour(spade.Behaviour.Behaviour):
        def _process(self):   
            msg = self._receive(True)
            # Check whether the message arrived
            if msg:
#                msgNote = serializer.deserialize(msg.content)
                print "UserOfflineBehaviour"
#                username = self.msg.sender.getName().split("@")[0]
#                self.myAgent.msgManager.add_msg_to_receivers(msgNote, [username], state=MsgState.TO_SEND)
            else:
                print "I waited but got no message"


# new send msg
    def sendMsg(self, message, receivers):
        self._sendMsg(message, receivers, new_msg_from_server_ontology)
# currently not in use    
    def updateMsg(self, message, receivers):
        self._sendMsg(message, receivers, update_msg_from_server_ontology)
        
    def _sendMsg(self, message, receivers, ontology):
        msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        dumpedMsg = serializer.serialize(message)
        for recipient in receivers:
            receiverName = recipient+"@"+self.getDomain()
            receiverAddresses = ["xmpp://"+recipient+"@"+self.getDomain()]
            receiver = spade.AID.aid(name=receiverName,addresses=receiverAddresses)
            msg.addReceiver(receiver)            # Add the message receiver                  
        msg.setPerformative("inform")        # Set the "inform" FIPA performative
        msg.setOntology(ontology)        # Set the ontology of the message content
        msg.setContent(dumpedMsg)        # Set the message content
        self.send(msg)

    def _setup(self):
        self.groups = groups.Group()
        # Add the "DefaultBehavior" as the default behaviour
        self.msgManager = MessageManager()
        self.setDefaultBehaviour(DefaultBehavior())        
        
        self.addBehaviour(ServerNewMessageBehaviour(), ServerNewMessageBehaviour.get_msg_template())
        self.addBehaviour(ServerUpdateMessageBehaviour(), ServerUpdateMessageBehaviour.get_msg_template())
        self.addBehaviour(SyncRespondBehaviour(), SyncRespondBehaviour.get_msg_template())
        
        # Prepare template for "UserOfflineBehaviour"
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(new_msg_from_server_ontology)
        mt = spade.Behaviour.MessageTemplate(template)
        self.addBehaviour(self.UserOfflineBehaviour(), mt)

    