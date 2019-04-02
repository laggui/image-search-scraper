from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSignal

from widgets import ImageButton

class PlusIcon(QWidget):
    """
    Plus icon widget with specified description text to its right
    """
    add = pyqtSignal()
    def __init__(self, text: str, size: int = 24, parent: QWidget = None):
        super().__init__(parent)
        # Layout
        hLayout = QHBoxLayout()
        plusIcon = ImageButton('plus', size, size)
        hLayout.addWidget(plusIcon)
        hLayout.addWidget(QLabel(text))
        hLayout.addStretch(1)
        self.setLayout(hLayout)

        # Connect button signal
        plusIcon.clicked.connect(self.add)