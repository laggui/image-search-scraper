from PyQt5.QtWidgets import QPushButton, QWidget
from PyQt5.QtCore import Qt, QSize

from widgets.utils import newIcon

class ImageButton(QPushButton):
    """
    Base class for a clickable image button
    """
    def __init__(self, icon: str, width: int = 18, height: int = 18, parent: QWidget = None):
        super().__init__(parent)
        self.setIcon(newIcon(icon))
        self.setIconSize(QSize(width, height))
        self.initStyleSheet()

    def initStyleSheet(self):
        self.setObjectName('ImageButton')
        self.setStyleSheet('#ImageButton{border: none;}')

    def enterEvent(self, event):
        self.setCursor(Qt.PointingHandCursor)