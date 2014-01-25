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

def trunc_str(text, max_chars):
    return len(text) > max_chars and text[:max_chars-2] + "..." or text

with open("%s/style.css" % os.path.dirname(gui.__file__)) as f:
    GLOBAL_STYLESHEET = f.read()
    
def color_style(nw_color, se_color):
    return GLOBAL_STYLESHEET + '''
        QWidget#note {
            background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
                stop:0 %s, stop:1 %s);
        }''' % (nw_color, se_color)

STYLES = {    
    'yellow': color_style('#E4E360', '#E8CA21'),
    'blue': color_style('#64DCF9', '#2399EC'),
    'green': color_style('#C0FF5F', '#6BCD13'),
    'orange': color_style('#F9BC5F', '#EC9222'),
    'pink': color_style('#FABFF8', '#F792E2'),
    'red': color_style('#FF7979', '#F45454'),
    'white': color_style('#EDEDED', '#E0E0E0')
}

