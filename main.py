from core_mock import *
from gui import * 

def main():
    
    client = Client()
    print client.msgBox.getMsgByState(MsgState.NEW)
    
    app = QApplication(sys.argv)
    
    loginWindow = LoginWindow()
    loginWindow.show()

    allNotes = []
    for _, msg in client.msgBox.getMsgAll().items():
        allNotes.append(SolidNote(msg))
    
    for note in allNotes: note.show()
        
    return app.exec_()


if __name__ == '__main__':
    main()
