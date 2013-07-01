# -*- coding: utf-8 -*-

import spade
import time
import random
import server

# TODO: wydajność, zmienić na int i dodać mapę nazw
STATE_NEW = "new"
STATE_VISIBLE = "visible"
STATE_TO_SEND = "to_send"
STATE_SENT = "sent"
STATE_REMOVED = "removed"


def create_ping_template():
    aclTemplate = spade.Behaviour.ACLTemplate()
    aclTemplate.setPerformative("inform")
    aclTemplate.setOntology("ping")
    aclTemplate.setLanguage("peanuts")
    return spade.Behaviour.MessageTemplate(aclTemplate)

class Message(object):
    # TODO: zabezpieczenie mid
    
    def __init__(self, text, expire, sender, recipients_list):
        self.text = text
        self.expire = expire
        
        if type(sender) == str:
            self.sender = sender
        elif type(sender) == server.UserAccount:
            self.sender = sender.name
        
        self.recipients_list = recipients_list
        
        self.mid = "%s_%s_%s" % (self.sender, time.time(), random.randint(0, 100)) # TODO: wydajn.
    
    def __str__(self):
        return self.text # TODO:
    