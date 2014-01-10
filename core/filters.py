from message_factory import MessageFactory
import datetime
import re

class FilterQueue:
    def __init__(self):
        self.queue = []
    def add_filter(self, filter_, associated_object):
        self.queue += [(filter_, associated_object)]
    def get_first_matching(self, msg):
        for filter_, associated_object in self.queue:
            if filter_.matches(msg):
                return associated_object
        return None
    def move_up(self, filter_):
        for i in range(len(self.queue)):
            if self.queue[i][0] == filter_:
                if i==0:
                    return
                tmp = self.queue[i]
                del self.queue[i]
                self.queue.insert(i-1, tmp)
                
    def move_down(self, filter_):
        for i in range(len(self.queue)):
            if self.queue[i][0] == filter_:
                if i==len(self.queue)-1:
                    return
                tmp = self.queue[i]
                del self.queue[i]
                self.queue.insert(i+1, tmp)    

class RegexFilter:
    def __init__(self, pattern):
        self.pattern = pattern
    def matches(self, msg):
        if re.match(self.pattern, msg.content, re.IGNORECASE):
            return True
        else:
            return False
        
class WordFilter:
    def __init__(self, words_csv):
        self.words_csv = words_csv
    def matches(self, msg):
        for word in self.words_csv.split(","):
            if word.strip().find(msg.content)!=-1:
                return True
        return False        

# class WordFilter:
#     def __init__(self, word):
#         self.word = word
#     def matches(self, msg):
#         if self.word.find(msg.content)!=-1:
#             return True
#         else:
#             return False


class ValidAtLeastFilter():
    def __init__(self, days):
        self.days = days
        
    def matches(self, msg):
        return msg.expire_date - datetime.datetime.now() >= datetime.timedelta(days = self.days) 

class ValidAtMostFilter():
    def __init__(self, days):
        self.days = days
        
    def matches(self, msg):
        return msg.expire_date - datetime.datetime.today() < datetime.timedelta(days = self.days) 

class SenderFilter():
    def __init__(self, sender):
        self.sender = sender
        
    def matches(self, msg):
        return msg.sender == self.sender 

class RecepientFilter():
    def __init__(self, recepient):
        self.recepient = recepient
        
    def matches(self, msg):
        return self.recepient in msg.recipients

class OrFilter:
    def __init__(self, filter_list):
        self.filter_list = filter_list
    def matches(self, msg):
        for f in self.filter_list:
            if f.matches(msg):
                return True
        return False

class AndFilter:
    def __init__(self, filter_list):
        self.filter_list = filter_list
    def matches(self, msg):
        for f in self.filter_list:
            if not f.matches(msg):
                return False
        return True

if __name__ == '__main__':
    msg_factory = MessageFactory()
    msg_factory.set_sender("ala@cats.pl")
    msg_factory.set_content("ilikecats")
    msg_factory.set_recipients(["cat@cheshire.uk", "dorothy@oz.com"])
    msg = msg_factory.build()
    
    re_filter1 = RegexFilter("ihate.*");
    print "regexfilter1 = ", re_filter1.matches(msg)
    
    re_filter2 = RegexFilter(".*cats");
    print "regexfilter2 = ", re_filter2.matches(msg)
    
    word_filter1 = WordFilter("doesanyonereadthis?, ilikecatz");
    print "wordfilter1 = ", word_filter1.matches(msg)
    
    word_filter2 = WordFilter("catsaretasty,  ilikecats");
    print "wordfilter2 = ", word_filter2.matches(msg)
    
    valid_at_least_filter = ValidAtLeastFilter(days=4)
    print "valid at least filter = ", valid_at_least_filter.matches(msg)
    
    valid_at_most_filter = ValidAtMostFilter(days=6)
    print "valid at most filter = ", valid_at_most_filter.matches(msg)
    
    
    or_filter = OrFilter([valid_at_least_filter, valid_at_most_filter])
    print "or filter = ", or_filter.matches(msg)
    
    and_filter = AndFilter([valid_at_least_filter, valid_at_most_filter])
    print "and filter = ", and_filter.matches(msg)
    
    recepient_filter1 = RecepientFilter("tea_party@wonderland.org")
    print "recepient filter1 = ", recepient_filter1.matches(msg)
    
    recepient_filter2 = RecepientFilter("cat@cheshire.uk")
    print "recepient filter2 = ", recepient_filter2.matches(msg)
    
    sender_filter1 = SenderFilter("ala@dogz.pl")
    print "sender filter1 = ", sender_filter1.matches(msg)
    
    sender_filter2 = SenderFilter("ala@cats.pl")
    print "sender filter2 = ", sender_filter2.matches(msg)
    
    # this is how filters can be structured in application
    # or_filter_with_senders, or_filter_with_recepients, word_filter, re_filter, and_filter_with_valid_from_valid_to_filters
    filter1 = OrFilter([OrFilter([sender_filter1]), OrFilter([recepient_filter1]), word_filter1, re_filter1, AndFilter([valid_at_least_filter, valid_at_most_filter])])
    print "ready2use filter1 = ", filter1.matches(msg)
    filter2 = OrFilter([OrFilter([sender_filter1]), OrFilter([recepient_filter1, recepient_filter2]), word_filter1, re_filter2, AndFilter([valid_at_least_filter, valid_at_most_filter])])
    print "ready2use filter2 = ", filter2.matches(msg)
    filter3 = OrFilter([OrFilter([sender_filter1, sender_filter2]), OrFilter([recepient_filter2]), word_filter2, re_filter2, AndFilter([valid_at_least_filter, valid_at_most_filter])])
    print "ready2use filter3 = ", filter3.matches(msg)
    
    q = FilterQueue()
    q.add_filter(filter1, "FF0000") # second object can be anything
    q.add_filter(filter2, "00FF00")
    q.add_filter(filter3, "0000FF")
    print q.get_first_matching(msg)
    q.move_up(filter3)
    print q.get_first_matching(msg)
