from client_agent import ClientAgent
from message_factory import MessageFactory

if __name__ == "__main__":
    a = ClientAgent("piotrek@127.0.0.1", "secret")
    a.start()
    factory = MessageFactory()
    factory.set_sender('piotrek')
    factory.set_content("informacja")
    factory.set_recipients(['kuba', 'marek'])
    a.sendMsg(factory.build())
    alive = True
    import time, sys
    while alive:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            alive=False
    a.stop()
    sys.exit(0)