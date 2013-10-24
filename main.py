#!/usr/bin/env python2.7

import sys

from PySide.QtGui import QApplication

from core_mock import PeanotesClient 
from gui import MainGui 

def main():    
    app = QApplication(sys.argv)
    client = PeanotesClient()
    gui = MainGui(client)
    return app.exec_()


if __name__ == '__main__':
    main()
