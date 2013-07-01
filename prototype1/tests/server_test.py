import unittest
from peanotes import server, messages

class Test(unittest.TestCase):
    
#     @unittest.skip("skipping")
    def test_accounts_create(self):
        a1 = server.UserAccount("kuba", "secret")
        a2 = server.UserAccount("ala", "secret")
        s = server.MessagesServer()
        s.add_account(a1)
        s.add_account(a2)
        
        assert(s.accounts_dict["kuba"] == a1)
        assert(s.accounts_dict["ala"] == a2)

    def test_server_message_dist(self):
        a1 = server.UserAccount("kuba", "secret")
        a2 = server.UserAccount("ala", "secret")
        s = server.MessagesServer()
        s.add_account(a1)
        s.add_account(a2)
        
        m1 = messages.Message("hello", 0, a1.name, ['ala'])
        a1.add_outgoing_message(m1)
        assert(m1.mid in a1.__m_dict__)
        
        s.update_dist_list()
        assert(m1.mid in s.msg_dist_dict)
        
        s.dist_all()
        assert(m1.mid in a2.__m_dict__)
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()