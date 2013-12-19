import pickle
    
def serialize(message):
    try:
        message.content = message.content.encode("utf-8")
    except UnicodeDecodeError:
        pass
    return pickle.dumps(message)
def deserialize(message):
    message = pickle.loads(message)
    try:
        message.content = message.content.decode("utf-8")
    except UnicodeDecodeError:
        pass
    return message