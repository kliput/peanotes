# -*- coding: utf-8 -*-

import datetime
import uuid

class MsgState():
    GUI = 0
    NEW = 1
    READ = 2
    TO_SEND = 3
    SENT = 4
    DELETED = 5

class Message():
    def __str__(self):
        return "Message[content=%s, sender=%s, recipients=%s, expire_date=%s, state=%s, msg_uuid=%s]" %(self.content, self.sender, self.recipients, self.expire_date, self.state, self.msg_uuid)

    def __init__(self, content, sender, recipients, create_date, expire_date, state, msg_uuid):
        '''
        content - tresc tesktowa
        recipients - lista adresatow i grup adresatow
        expire_date - data waznosci
        state - stan typu MsgState
        msg_uuid - unikalne id wiadomosci
        '''
        assert isinstance(expire_date, datetime.datetime)
        
        self.content = content
        self.sender = sender
        self.recipients = recipients
        self.create_date = create_date
        self.expire_date = expire_date
        self.state = state
        self.msg_uuid = msg_uuid


class MessageFactory(object):
    '''
    classdocs
    '''
    POLICY_EXPIREDATE_DAYS = 1
    POLICY_EXPIREDATE_DATE = 2

    def __init__(self):
        '''
        Constructor
        '''
        self.days_to_expire = 7
        self.content = ""
        self.policy = MessageFactory.POLICY_EXPIREDATE_DAYS
        self.state = MsgState.NEW
        self.recipients = []
    def set_content(self, content):
        self.content = content
    def set_sender(self, sender):
        self.sender = sender
    def set_recipients(self, recipients):
        self.recipients = recipients
    def set_expiredate_policy(self, policy):
        self.policy = policy
    def set_expiredate(self, expire_date):
        self.expire_date = expire_date
    def set_days_to_expire(self, days_to_expire):
        self.days_to_expire = days_to_expire
    def set_state(self, state):
        self.state = state
    def build(self):
        if self.policy == self.POLICY_EXPIREDATE_DAYS or self.expire_date is None:
            expire_date = datetime.datetime.today() + datetime.timedelta(days=7)
        else:  # self.policy==self.POLICY_EXPIREDATE_DATE:
            expire_date = self.expire_date
        return Message(self.content, self.sender, self.recipients, datetime.datetime.today(), expire_date, self.state, uuid.uuid4())
        # return Message(content, sender,
        
if __name__ == "__main__":
    factory = MessageFactory()
    factory.set_sender('piotrek')
    factory.set_content(u'Inna wiadomość')
    factory.set_recipients(['marek', 'kuba'])
    print factory.build()
