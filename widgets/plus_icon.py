from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from widgets import ImageButton

class PlusIcon(QWidget):
    """
    Plus icon widget with specified description text to its right
    """
    def __init__(self, text: str, size: int = 24, parent: QWidget = None):
        super().__init__(parent)
        # Layout
        hLayout = QHBoxLayout()
        self.plusIcon = ImageButton('plus', size)
        hLayout.addWidget(self.plusIcon)
        hLayout.addWidget(QLabel(text))
        hLayout.addStretch(1)
        self.setLayout(hLayout)

    def clickableIcon(self):
        """Returns the clickable icon in order to access its clicked signal externally"""
        return self.plusIcon