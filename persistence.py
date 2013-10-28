from message_factory import Message, MsgState
import copy
import pickle
class MessageManager(object):

    def __init__(self):
        '''
        Constructor
        '''
        # !!! very silly persistence !!!
        self.userData = self._loadData()
    def add_msg_to_sender(self, message, state=MsgState.SENT):
        self._create_users_if_not_exist(message)
        msg_copy = copy.deepcopy(message)
        msg_copy.state = state
        self.userData[message.sender][message.msg_uuid] = msg_copy
        # !!! very silly persistence !!!
        self._persistData(self.userData)
    
    def add_msg_to_users(self, message, users, state=MsgState.NEW):
        self._create_users_if_not_exist(message)
        for user in users:
            msg_copy = copy.deepcopy(message)
            msg_copy.state = state
            self.userData[user][message.msg_uuid] = msg_copy
        # !!! very silly persistence !!!
        self._persistData(self.userData)
        
    def _create_users_if_not_exist(self, message):
        users = [message.sender] + message.recipients
        for user in users:
            if not self.userData.has_key(user):
                self.userData[user] = {}
    def get_msgs_for_username(self, username, state=None):
        return self.userData[username]


    def _loadData(self):
        data = None
        try:
            with open('server_userdata.pkl', 'rb') as file_:
                data = pickle.load(file_)
        except IOError:
            data = {}
        return data
    
    def _persistData(self, data):
        try:
            with open('server_userdata.pkl', 'wb') as file_:
                pickle.dump(data, file_)
        except IOError, e:
            print e