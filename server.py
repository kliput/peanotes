#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
from agents.server_agent import ServerAgent

if __name__ == "__main__":
    a = ServerAgent("message.server@"+sys.argv[1], "secret")
    #a.wui.start()
    a.setDebugToScreen()
    a.start()
    
    try:
        while True:
            raw_input('')
    except KeyboardInterrupt:
        pass
    
    a.stop()
    sys.exit(0)
    