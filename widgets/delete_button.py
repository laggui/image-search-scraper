from PyQt5.QtWidgets import QWidget

from widgets import ImageButton

class DeleteButton(ImageButton):
    """
    Delete image button with personalized style sheet
    """
    def __init__(self, size: int = 18, parent: QWidget = None):
        super().__init__('delete', size, size, parent)

    def initStyleSheet(self):
        self.setObjectName('DeleteButton')
        self.setStyleSheet('#DeleteButton{border: none; padding: 1px;} #DeleteButton:hover{background: rgba(0, 0, 0, 10%);}')