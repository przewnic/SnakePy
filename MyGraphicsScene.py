# Author: przewnic

from PyQt5 import QtWidgets
from PyQt5 import QtCore


class MyGraphicsScene(QtWidgets.QGraphicsScene):
    mouse_hover_pos = QtCore.pyqtSignal(QtCore.QPointF)
    mouse_clicked_pos = QtCore.pyqtSignal(QtCore.QPointF)

    def __init__(self, parent):
        super(MyGraphicsScene, self).__init__(parent)
        self.mouse_pressed = False

    def mousePressEvent(self, event):
        self.mouse_pressed = True
        pos = event.lastScenePos()
        self.mouse_clicked_pos.emit(pos)

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

    def mouseMoveEvent(self, event):
        if self.mouse_pressed:
            pos = event.lastScenePos()
            self.mouse_hover_pos.emit(pos)
