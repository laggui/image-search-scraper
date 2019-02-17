from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from enum import Enum

from widgets import DeleteButton, PlusIcon, SearchBox, TextBox

class SupportedSearchClients(Enum):
    GOOGLE = 0
    BING = 1

class SearchClient(QGroupBox):
    """
    Search API Client groupbox widget layout
    """
    _titles = {SupportedSearchClients.GOOGLE: 'Google Custom Search JSON API',
              SupportedSearchClients.BING: 'Bing Image Search API v7'}
    def __init__(self, client: SupportedSearchClients, parent: QWidget = None):
        super().__init__(self._titles[client], parent)
        # pal = QPalette()
        # pal.setColor(QPalette.Background, QColor.fromRgba64(0, 0, 0, (65535/100)*3))
        # self.setAutoFillBackground(True)
        # self.setPalette(pal)
        self.client = client
        self.searchCount = 1
        self.maxResults = 500

        self.setContentsMargins(11, 3, 3, 11)
        
        # Main vertical layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(0, 0, 6, 0)

        # Delete button and its layout
        deleteLayout = QHBoxLayout()
        deleteLayout.setAlignment(Qt.AlignRight)
        deleteLayout.setContentsMargins(0, 6, 0, 0)
        self.deleteButton = DeleteButton()
        deleteLayout.addWidget(self.deleteButton)
        self.mainLayout.addLayout(deleteLayout)

        # API keys text boxes
        keysLayout = QHBoxLayout()
        self.apiKey = TextBox('Enter your API key here...')
        keysLayout.addWidget(self.apiKey)
        if self.client == SupportedSearchClients.GOOGLE:
            self.cseID = TextBox('Google Custom Search Engine ID...')
            keysLayout.addWidget(self.cseID)
            self.maxResults = 100
        keysLayout.addStretch(1)        
        self.mainLayout.addLayout(keysLayout)

        # Search queries layout
        self.queriesLayout = QVBoxLayout()
        # Add search box
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}')
        self.queriesLayout.addWidget(searchBox)
        self.mainLayout.addLayout(self.queriesLayout)

        # Add plus icon
        addQuery = PlusIcon('Query', size=20)
        self.mainLayout.addWidget(addQuery)

        self.mainLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Connect signals and slots
        self.deleteButton.clicked.connect(self.destroy)
        searchBox.delete.connect(self.updateSearchBoxTitles)
        addQuery.clickableIcon().clicked.connect(self.addSearchBox)

    def updateSearchBoxTitles(self):
        self.searchCount -= 1
        i = self.searchCount - 1
        for s in self.queriesLayout.parentWidget().findChildren(SearchBox):
            if not s.deleteInProgress:
                s.setProperties(f'Query #{self.searchCount - i}')
                i -= 1

    def addSearchBox(self):
        self.searchCount += 1
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}')
        self.queriesLayout.addWidget(searchBox)
        searchBox.delete.connect(self.updateSearchBoxTitles)

    def _clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clearLayout(item.layout())

    @pyqtSlot()
    def destroy(self):
        # Delete all items in the main layout
        self._clearLayout(self.mainLayout)
        # Delete self
        self.deleteLater()