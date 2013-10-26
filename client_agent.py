#!/usr/bin/python2.7
import spade
import pickle
import serializer
from message_factory import Message, MessageFactory
import datetime

class MyAgent(spade.Agent.Agent):
    
    class HandleMessageBehaviour(spade.Behaviour.Behaviour):
        def _process(self):
            msg = None
            # Blocking receive indefinitely
            msg = self._receive(True)
            if msg: # Check whether the message arrived
                msgNote = serializer.deserialize(msg.content)
                print msgNote
                #msgManager.addMsg(msgNote)
            else:
                print "No msg"
    def _setup(self):
        print "MyAgent starting . . ."
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("message-sent")        # Set the ontology of the message content
        mt = spade.Behaviour.MessageTemplate(template)
        gmb = self.HandleMessageBehaviour()
        # Add the behaviour WITH the template
        self.addBehaviour(gmb, mt)                
#       
    def sendMsg(self, message):
        dumpedMsg = serializer.serialize(message)
        
        msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        msg.setPerformative("inform")        # Set the "inform" FIPA performative
        msg.setOntology("message")        # Set the ontology of the message content
        msg.setLanguage("python-pickle")              # Set the language of the message content
        receiver = spade.AID.aid(name="message.server@127.0.0.1", 
                                     addresses=["xmpp://message.server@127.0.0.1"])
        msg.addReceiver(receiver)            # Add the message receiver
        msg.setContent(dumpedMsg)        # Set the message content
        self.send(msg)
        
if __name__ == "__main__":
    a = MyAgent("piotrek@127.0.0.1", "secret")
    a.start()
    a2 = MyAgent("kuba@127.0.0.1", "secret")
    a2.start()
    factory = MessageFactory()
    factory.set_sender('piotrek')
    factory.set_content("informacja")
    factory.set_recipients(['kuba', 'marek'])
    a.sendMsg(factory.build())