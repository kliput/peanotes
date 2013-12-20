#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys

from PySide.QtGui import QApplication
from xmpp.protocol import HostUnknown

from core.peanotes_client import PeanotesClient 
from gui.main_gui import MainGui 

def main():
    if len(sys.argv) < 2:
        print 'Usage: ./client.py <user_jid>\nWhere <user_jid> is in form: login@server, like: kowalski@192.168.1.1'
        return 1
    else:
        app = QApplication(sys.argv)
        try:
            client = PeanotesClient(sys.argv[1], "secret")
        except HostUnknown as e:
            print 'No XMPP server detected on provided address.'
            return 1
        else:
            gui = MainGui(client)
            return app.exec_()


if __name__ == '__main__':
    main()
