#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import spade
import messages

class UserAccount(object):
	def __init__(self, name, password):
		# mapa: id wiadomości -> (wiadomość, stan)
		self.__m_dict__ = {}
		
		self.add_listeners = {self.al_console_notify}
		self.change_listeners = {}
		
		self.name = name
		self.password = password
	
	def __msg_add__(self, message, state):
		if message.mid in self.__m_dict__:
			print "error: duplicate message: %s to: %s" % (message.mid, self.name)
# 			raise Exception("message already exists: %s" % (message))
		self.__m_dict__[message.mid] = (message, state)
		map(lambda f: f(message, state), self.add_listeners)
	
	def __msg_change__(self, mid, state):
		if id not in self.__m_dict__:
			print "error: changing message state: %s in: %s" % (mid, self.name)
# 			raise Exception("message not exists: %s" % (message.mid))
		self.__m_dict__[mid][1] = state
		map(lambda f: f(self.__m_dict__[mid]), self.change_listeners)
	
	def add_incoming_message(self, message):
		self.__msg_add__(message, messages.STATE_NEW)
	
	def add_outgoing_message(self, message):
		self.__msg_add__(message, messages.STATE_TO_SEND)
	
	def message_to_visible(self, mid):
		self.__msg_change__(mid, messages.STATE_VISIBLE)
	
	def message_to_sent(self, mid):
		self.__msg_change__(mid, messages.STATE_SENT)
	
	def message_to_removed(self, mid):
		self.__msg_change__(mid, messages.STATE_REMOVED)

	## -- listeners: fun(message, state) --
	def al_console_notify(self, m, s):
		print "-- adding %s message for: %s --" % (s, self.name)
		print "id: %s, expire: %s, sender: %s\ntext: [%s]" % (m.mid, m.expire, m.sender, m.text)

	# TODO: metoda do informacji o zmianach
	# co potrzeba do aktualizacji?
	# - id wiadomości, stan 

	# synchronizuje z innym katalogiem położonym na innym agencie
	# 
	def update(self, m_cat):
		'''
		Updates catalogue with m_cat object.
		m_cat should be newer than self.
		'''
		# TODO: prawdziwa aktualizacja na podstawie diffów
		pass


class MessagesServer(object):
	def __init__(self):
		self.groups_dict = {} # mapa: nazwa grupy -> lista członków
		self.accounts_dict = {} # mapa: nazwa konta -> (konto)
		self.msg_dist_dict = {} # wiadomości do dystrybucji: id -> (wiadomość)
	
	def add_account(self, account):
		name = account.name
		if name in self.accounts_dict:
			raise Exception("account already exists: %s" % (name))
		self.accounts_dict[name] = account
	
	def update_dist_list(self):
		to_send = []
		for account in self.accounts_dict.itervalues():
			to_send.extend([t[0] for t in account.__m_dict__.itervalues() if t[1] == messages.STATE_TO_SEND])
		for msg in to_send:
			mid = msg.mid
			if mid not in self.msg_dist_dict:
				self.msg_dist_dict[mid] = msg
						
	
	def dist_all(self):
		for message in self.msg_dist_dict.itervalues():
			for recipient in message.recipients_list:
				try:
					# nazwa grupy
					if recipient in self.groups_dict:
						for g_rec in self.groups_dict[recipient]:
							self.accounts_dict[g_rec].add_incoming_message(message)
					# zwyczajna nazwa
					else:
						self.accounts_dict[recipient].add_incoming_message(message)
				except KeyError as e:
					print "there is not such account: %s" % e.message 
	
class ServerAgent(spade.Agent.Agent):
	class PongBehaviour(spade.Behaviour.EventBehaviour):
		def _process(self):
			print 'Pong processing waiting...'
			msg = self._receive(True)
			print 'Pong processing received...'
			if msg:
				print 'Pong message: %s' % (msg)
			else:
				print 'No message!'
			
	def _setup(self):
		print "Server agent starting..."
		self.messages_server = MessagesServer()
		self.addBehaviour(ServerAgent.PongBehaviour(), messages.create_ping_template())

# --------

		
if __name__ == "__main__":
	a = ServerAgent("server@127.0.0.1", "secret")
	a.setDebugToScreen()
	a.start()
