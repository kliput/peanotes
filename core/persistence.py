from core.message_factory import Message, MsgState
import copy
import pickle

SERVER_USERDATA_PATH = 'user_data/server_userdata.pkl'

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
        if username in self.userData:
            return self.userData[username]
        else:
            return {}

    def _loadData(self):
        data = None
        try:
            with open(SERVER_USERDATA_PATH, 'rb') as file_:
                data = pickle.load(file_)
        except IOError:
            data = {}
        return data
    
    def _persistData(self, data):
        try:
            with open(SERVER_USERDATA_PATH, 'wb') as file_:
                pickle.dump(data, file_)
        except IOError, e:
            print e