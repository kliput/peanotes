import pickle
    
def serialize(message):
    return pickle.dumps(message)
def deserialize(message):
    return pickle.loads(message)