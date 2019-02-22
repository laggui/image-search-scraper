from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from enum import Enum

from widgets import DeleteButton, PlusIcon, SearchBox, TextBox

class SupportedSearchClients(Enum):
    GOOGLE = 0
    GOOGLE_API = 1
    BING_API = 2

class SearchClient(QGroupBox):
    """
    Search Client groupbox widget layout
    """
    delete = pyqtSignal()
    searchCountUpdated = pyqtSignal(int, str)
    _titles = {SupportedSearchClients.GOOGLE: 'Google Image Scraper',
               SupportedSearchClients.GOOGLE_API: 'Google Custom Search JSON API',
               SupportedSearchClients.BING_API: 'Bing Image Search API v7'}
    def __init__(self, client: SupportedSearchClients, saveDirectory: str, parent: QWidget = None):
        super().__init__(self._titles[client], parent)
        self.client = client
        self.searchCount = 1
        self.maxResults = 25000
        self.defaultSaveDirectory = saveDirectory

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
        if self.client == SupportedSearchClients.GOOGLE_API or self.client == SupportedSearchClients.BING_API:
            keysLayout = QHBoxLayout()
            self.apiKey = TextBox('Enter your API key here...')
            keysLayout.addWidget(self.apiKey)
            if self.client == SupportedSearchClients.GOOGLE_API:
                self.cseID = TextBox('Google Custom Search Engine ID...')
                keysLayout.addWidget(self.cseID)
                self.maxResults = 100
            keysLayout.addStretch(1)        
            self.mainLayout.addLayout(keysLayout)

        # Search queries layout
        self.queriesLayout = QVBoxLayout()
        # Add search box
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}', self.defaultSaveDirectory)
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

    def setDefaultSaveDirectory(self, directory: str):
        self.defaultSaveDirectory = directory
        for s in self.queriesLayout.parentWidget().findChildren(SearchBox):
            s.setSaveDirectory(directory)

    def addSearchBox(self):
        self.searchCount += 1
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}', self.defaultSaveDirectory)
        self.queriesLayout.addWidget(searchBox)
        searchBox.delete.connect(self.updateSearchBoxTitles)
        self.searchCountUpdated.emit(1, 'added')

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
    def updateSearchBoxTitles(self):
        self.searchCount -= 1
        i = self.searchCount - 1
        for s in self.queriesLayout.parentWidget().findChildren(SearchBox):
            if not s.deleteInProgress:
                s.setProperties(f'Query #{self.searchCount - i}')
                i -= 1
        self.searchCountUpdated.emit(1, 'removed') # removed one search box

    @pyqtSlot()
    def destroy(self):
        # Delete all items in the main layout
        self._clearLayout(self.mainLayout)
        # Delete self
        self.deleteLater()
        self.delete.emit()
        self.searchCountUpdated.emit(self.searchCount, 'removed')