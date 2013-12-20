#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
import spade
from core import serializer
from agents.behaviours import *

class ClientAgent(spade.Agent.Agent):
    def __init__(self, jid, password, peaClient=None):
        self.peaClient = peaClient
        self.jid = jid
        self.peaClient = peaClient
        spade.Agent.Agent.__init__(self, jid, password)
      
    def _setup(self):
        print "ClientAgent starting . . ."
        self.addBehaviour(ClientNewMessageBehaviour(), ClientNewMessageBehaviour.get_msg_template())        
        self.addBehaviour(SyncRequestBehaviour())

    def sendMsg(self, message):
        self._sendMsg(message, new_msg_to_server_ontology)

    def updateMsg(self, message):
        self._sendMsg(message, update_msg_to_server_ontology)
    
    def _sendMsg(self, message, ontology):
        dumpedMsg = serializer.serialize(message)
        
        msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        msg.setPerformative("inform")        # Set the "inform" FIPA performative
        msg.setOntology(ontology)
        receiver = spade.AID.aid(name="message.server"+"@"+self.getDomain(), 
                                     addresses=["xmpp://message.server"+"@"+self.getDomain()])
        msg.addReceiver(receiver)            # Add the message receiver
        msg.setContent(dumpedMsg)        # Set the message content
        self.send(msg)