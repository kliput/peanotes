# -*- coding: utf-8 -*-
# TODO: DEPRECATED?
from agents.client_agent import ClientAgent
from core.message_factory import MessageFactory
import sys
if __name__ == "__main__":
    a = ClientAgent("piotrek@"+sys.argv[1], "secret")
    a.start()
    factory = MessageFactory()
    factory.set_sender('piotrek')
    factory.set_content(sys.argv[2])
    #factory.set_recipients(['kuba', 'marek'])
    factory.set_recipients(['kuba'])
    a.sendMsg(factory.build())
    alive = True
    import time
    while alive:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            alive=False
    a.stop()
    sys.exit(0)