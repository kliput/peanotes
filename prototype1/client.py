#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import spade
import time
import re
import time

from spade import *

class InitBehaviour(Behaviour.OneShotBehaviour):
	def __init__(self, serverReceiver):
		Behaviour.OneShotBehaviour.__init__(self)
		self.serverReceiver = serverReceiver
	
	def onStart(self):
		print "Init started."
	
	def _process(self):
		print "Processing started"
		
		for _ in range(5):
			msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
			msg.setPerformative("inform")        # Set the "inform" FIPA performative
			msg.setOntology("ping")        # Set the ontology of the message content
			msg.setLanguage("peanuts")       # Set the language of the message content
			msg.addReceiver(self.serverReceiver)            # Add the message receiver
			msg.setContent("ping")        # Set the message content
			
			self.myAgent.send(msg)
			
			time.sleep(3)
			
		print "Processing ended"
	
	def onEnd(self):
		print "End."
		self.myAgent.stop()

class ClientAgent(Agent.Agent):
	def _setup(self):
		print "Client setup..."
		#self.setDebugToScreen()
		adr = 'server@127.0.0.1'
		serverReceiver = spade.AID.aid(name=adr, addresses=["xmpp://%s" % (adr)])
		self.addBehaviour(InitBehaviour(serverReceiver), None)
		
		
if __name__ == "__main__":
	name = sys.argv[1]
	a = ClientAgent("%s@127.0.0.1" % (name), "secret")
	a.setDebugToScreen()
	a.start()
	