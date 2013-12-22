# -*- coding: utf-8 -*-

from PySide.QtGui import QPixmap, QIcon, QApplication

import os, gui # self import for module path
IMAGES_PATH = "%s/images" % os.path.dirname(gui.__file__)
def image_path(file_name):
    return "%s/%s" % (IMAGES_PATH, file_name)

def create_icon_png(name):
    return QIcon(image_path("%s.png" % name))

def pea_app():
    return QApplication.instance()

def list_widget_items(list_widget):
    'Pomocniczo dla QListWidget: zwraca listę itemów'
    return [list_widget.item(i) for i in range(list_widget.count())]

with open("%s/style.css" % os.path.dirname(gui.__file__)) as f:
    GLOBAL_STYLESHEET = f.read()
    