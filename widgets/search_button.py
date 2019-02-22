from PyQt5.QtWidgets import QWidget

from widgets import ImageButton

class SearchButton(ImageButton):
    """
    Search and download image button with personalized style sheet
    """
    def __init__(self, size: int = 28, parent: QWidget = None):
        super().__init__('search-download', size, size, parent)
        self.setToolTip('Search & Download')

    def initStyleSheet(self):
        self.setObjectName('SearchButton')
        self.setStyleSheet('#SearchButton{border: none; padding: 1px;} #SearchButton:hover{background: rgba(0, 0, 0, 10%);}')