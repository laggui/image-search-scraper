from PyQt5.QtWidgets import QTextEdit, QWidget
from PyQt5.QtCore import Qt

__textheight__ = 25

class TextBox(QTextEdit):
    """
    Basic textbox widget with fixed height and placeholder text
    """
    def __init__(self, placeHolderText: str, textHeight: int = __textheight__, parent: QWidget = None):
        super().__init__(parent)
        self.setFixedHeight(textHeight)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setPlaceholderText(placeHolderText)