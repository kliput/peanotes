#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import spade
import time

class ServerAgent(spade.Agent.Agent):
	class PongBehaviour(spade.Behaviour.EventBehaviour):
		def _process(self):
			msg = None
			print 'Pong processing waiting...'
			msg = self._receive(True)
			print 'Pong processing received...'
			if msg:
				print 'Pong message: %s' % (msg)
			else:
				print 'No message!'
	
	def _setup(self):
		print "Server starting . . ."
		
		# Create the template for the EventBehaviour: a message from myself
		aclTemplate = spade.Behaviour.ACLTemplate()
		aclTemplate.setPerformative("inform")        # Set the "inform" FIPA performative
		aclTemplate.setOntology("ping")        # Set the ontology of the message content
		aclTemplate.setLanguage("peanuts")       # Set the language of the message content
		messageTemplate = spade.Behaviour.MessageTemplate(aclTemplate)
		
		# Add the EventBehaviour with its template
		self.addBehaviour(self.PongBehaviour(), messageTemplate)
		
if __name__ == "__main__":
	a = ServerAgent("server@127.0.0.1", "secret")
	a.setDebugToScreen()
	a.start()
