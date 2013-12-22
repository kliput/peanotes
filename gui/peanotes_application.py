from PySide.QtGui import QApplication

from gui.utils import create_icon_png

class PeanotesApplication(QApplication):
    def __init__(self, *args, **kwargs):
        super(PeanotesApplication, self).__init__(*args, **kwargs)
        
        self.send_icon = create_icon_png("send")
        self.tray_icon = create_icon_png("icon")
        self.close_icon = create_icon_png("close")
        self.calendar_icon = create_icon_png("calendar")
        self.add_icon = create_icon_png("list-add")
        