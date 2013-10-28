from client_agent import ClientAgent

import sys

if __name__ == '__main__':
    a = ClientAgent(sys.argv[1], "secret")
    a.start()
    alive = True
    import time, sys
    while alive:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            alive=False
    
    a.stop()
    sys.exit(0)