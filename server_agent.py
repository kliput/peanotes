#!/usr/bin/python2.7
import spade
import serializer

class MyAgent(spade.Agent.Agent):
    
    server_address = "127.0.0.1"
    
    class ReceiveBehav(spade.Behaviour.Behaviour):
        """This behaviour will receive all kind of messages"""
        def _process(self):
            self.msg = None     
            # Blocking receive for 10 seconds
            self.msg = self._receive(True, 10)
            # Check wether the message arrived
            if self.msg:
                print "Default msg handling"
                print self.msg.receivers
                #print self.msg
            else:
                print "I waited but got no message"

    class HandleMessageBehaviour(spade.Behaviour.Behaviour):
        def _process(self):
            msg = None
            # Blocking receive indefinitely
            msg = self._receive(True)
            if msg: # Check whether the message arrived
                msgNote = serializer.deserialize(msg.content)
                print msgNote
                #msgManager.addMsg(msgNote)
                  
                print msgNote.recipients
                self.myAgent.sendMsg(msgNote)
                

            else:
                print "No msg"                
                
    def sendMsg(self, message):
        msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
        dumpedMsg = serializer.serialize(message)
        print msg.receivers
        msg.resetReceivers()
        for recipient in message.recipients:
            
            receiverName = recipient+"@"+self.server_address
            receiverAddresses = ["xmpp://"+recipient+"@"+self.server_address]
            print "receiverAddr = ", receiverAddresses
            receiver = spade.AID.aid(name=receiverName,addresses=receiverAddresses)
            msg.addReceiver(receiver)            # Add the message receiver                  
        msg.setPerformative("inform")        # Set the "inform" FIPA performative
        msg.setOntology("message-sent")        # Set the ontology of the message content
        msg.setLanguage("python-pickle")              # Set the language of the message content
        msg.setContent(dumpedMsg)        # Set the message content
        self.send(msg)

    def _setup(self):
        # Add the "ReceiveBehav" as the default behaviour
        rb = self.ReceiveBehav()
        self.setDefaultBehaviour(rb)        
        # Prepare template for "handleMessageBehaviour"
        template = spade.Behaviour.ACLTemplate()
        template.setOntology("message")        # Set the ontology of the message content
        mt = spade.Behaviour.MessageTemplate(template)
        gmb = self.HandleMessageBehaviour()
        # Add the behaviour WITH the template
        self.addBehaviour(gmb, mt)                

if __name__ == "__main__":
    a = MyAgent("message.server@127.0.0.1", "secret")
    #a.start()
    a.run();