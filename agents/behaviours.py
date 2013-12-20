# -*- coding: utf-8 -*-
import spade.Behaviour
from core import serializer
import sys
import traceback
from core.message_factory import MsgState
from spade.Behaviour import OneShotBehaviour
# Default behaviour
class DefaultBehavior(spade.Behaviour.Behaviour):
    def _process(self):
        self.msg = None     
        self.msg = self._receive(True)
        if self.msg:
            print "Default msg handling"
        else:
            print "I waited but got no message"

#Synchronization
sync_ontology = "request-sync"             
class SyncRespondBehaviour(spade.Behaviour.Behaviour): # Server
    @staticmethod
    def get_msg_template():
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(sync_ontology)
        return spade.Behaviour.MessageTemplate(template)
    def _process(self):
        self.msg = None     
        self.msg = self._receive(True)
        if self.msg:
            try:
                username = self.msg.sender.getName().split("@")[0]
                print "SyncRespondBehaviour triggered by user=", username
                msgNotes = self.myAgent.msgManager.get_msgs_for_username(username)
                for msgNote in msgNotes.values():
                    self.myAgent.sendMsg(msgNote, [username])
            except Exception:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=5, file=sys.stdout)
        else:
            print "I waited but got no message"
            
class SyncRequestBehaviour(spade.Behaviour.OneShotBehaviour):
        
    def _process(self):
        msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        msg.setPerformative("inform")        # Set the "inform" FIPA performative
        msg.setOntology(sync_ontology)        # Set the ontology of the message content
        receiver = spade.AID.aid(name="message.server"+"@"+self.myAgent.getDomain(), 
                                 addresses=["xmpp://message.server"+"@"+self.myAgent.getDomain()])
        msg.addReceiver(receiver)            # Add the message receiver
        #msg.setContent(dumpedMsg)        # Set the message content
        self.myAgent.send(msg)
        
#new message
new_msg_from_server_ontology = "new-message-from-server"
new_msg_to_server_ontology = "new-message-to-server"
class ServerNewMessageBehaviour(spade.Behaviour.Behaviour):
    @staticmethod
    def get_msg_template():
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(new_msg_to_server_ontology)
        return spade.Behaviour.MessageTemplate(template)
    def _process(self):
        # Blocking receive indefinitely
        msg = self._receive(True)
        if msg: # Check whether the message arrived
            msgNote = serializer.deserialize(msg.content)
            print "new msg arrived, =", msgNote
            self.myAgent.msgManager.add_msg_to_sender(msgNote, state=MsgState.SENT)
            self.myAgent.msgManager.add_msg_to_users(msgNote, msgNote.recipients, state=MsgState.NEW)  
            msgNote.state = MsgState.NEW
            self.myAgent.sendMsg(msgNote, msgNote.recipients)
        else:
            print "No msg"
            
class ClientNewMessageBehaviour(spade.Behaviour.Behaviour):
    @staticmethod
    def get_msg_template():
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(new_msg_from_server_ontology)
        return spade.Behaviour.MessageTemplate(template)
    def _process(self):
        # Blocking receive indefinitely
        msg = self._receive(True)
        if msg: # Check whether the message arrived
            msgNote = serializer.deserialize(msg.content)
            print msgNote
            self.myAgent.peaClient.agentUpdated([msgNote])
            
# these lines were added to check, if updating msg on server works correctly
# at the time it worked, so if nothing changes the code can be used to update message state
#            msgNote.state = MsgState.READ 
#            self.myAgent.updateMsg(msgNote)

# it is the right place to do sth with the message - either add it to msgBox, or execute some listener
# with msgNote as parameter
#            self.myAgent.msgBox.addMsg(...)
        else:
            print "No msg"



#new message
update_msg_from_server_ontology = "update-message-from-server"
update_msg_to_server_ontology = "update-message-to-server"
class ServerUpdateMessageBehaviour(spade.Behaviour.Behaviour):
    @staticmethod
    def get_msg_template():
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(update_msg_to_server_ontology)
        return spade.Behaviour.MessageTemplate(template)
    def _process(self):
        # Blocking receive indefinitely
        msg = self._receive(True)
        if msg: # Check whether the message arrived
            msgNote = serializer.deserialize(msg.content)
            print "updated msg arrived, =", msgNote
            #self.myAgent.msgManager.add_msg_to_sender(msgNote, state=msgNote.state)
            username = msg.sender.getName().split("@")[0]
            self.myAgent.msgManager.add_msg_to_users(msgNote, [username],state=msgNote.state)
        else:
            print "No msg"

# not needed yet            
class ClientUpdateMessageBehaviour(spade.Behaviour.Behaviour):
    @staticmethod
    def get_msg_template():
        template = spade.Behaviour.ACLTemplate()
        template.setOntology(update_msg_from_server_ontology)
        return spade.Behaviour.MessageTemplate(template)
    def _process(self):
        # Blocking receive indefinitely
        msg = self._receive(True)
        if msg: # Check whether the message arrived
            msgNote = serializer.deserialize(msg.content)
            print msgNote
            #msgManager.addMsg(msgNote)
        else:
            print "No msg"
