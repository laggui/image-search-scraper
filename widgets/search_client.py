from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QSpinBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot

from widgets import DeleteButton, PlusIcon, SearchBox, TextBox

from webscraper import SupportedSearchClients

class SearchClient(QGroupBox):
    """
    Search Client groupbox widget layout
    """
    delete = pyqtSignal()
    searchCountUpdated = pyqtSignal(int, str)
    search = pyqtSignal([str, str, str, str, int], [str, str, str, int], [str, str, int])
    _titles = {SupportedSearchClients.GOOGLE: 'Google Image Scraper',
               SupportedSearchClients.GOOGLE_API: 'Google Custom Search JSON API',
               SupportedSearchClients.BING_API: 'Bing Image Search API v7'}
    def __init__(self, client: SupportedSearchClients, saveDirectory: str, parent: QWidget = None):
        super().__init__(self._titles[client], parent)
        self.client = client
        self.searchCount = 1
        self.maxResults = 25000
        self.defaultSaveDirectory = saveDirectory

        self.setContentsMargins(11, 3, 0, 11)
        
        # Main vertical layout
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setAlignment(Qt.AlignTop)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Delete button and its layout
        deleteLayout = QHBoxLayout()
        deleteLayout.setAlignment(Qt.AlignRight)
        deleteLayout.setContentsMargins(0, 6, 0, 0)
        self.deleteButton = DeleteButton()
        deleteLayout.addWidget(self.deleteButton)
        self.mainLayout.addLayout(deleteLayout)

        # Client layout
        clientLayout = QVBoxLayout()
        clientLayout.setAlignment(Qt.AlignTop)
        clientLayout.setContentsMargins(0, 0, 11, 0)
        self.mainLayout.addLayout(clientLayout)

        # API keys text boxes
        if self.client == SupportedSearchClients.GOOGLE_API or self.client == SupportedSearchClients.BING_API:
            keysLayout = QHBoxLayout()
            self.apiKey = TextBox('Enter your API key here...')
            self.apiKey.textChanged.connect(self.updateSearchBoxEnabledState)
            keysLayout.addWidget(self.apiKey)
            if self.client == SupportedSearchClients.GOOGLE_API:
                self.cseID = TextBox('Google Custom Search Engine ID...')
                self.cseID.textChanged.connect(self.updateSearchBoxEnabledState)
                keysLayout.addWidget(self.cseID)
                self.maxResults = 100
            keysLayout.addStretch(1)
            clientLayout.addLayout(keysLayout)

        # Initial search related widgets state
        self.initState = self.client != SupportedSearchClients.GOOGLE_API and self.client != SupportedSearchClients.BING_API

        # Search queries layout
        self.queriesLayout = QVBoxLayout()
        # Add search box
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}', self.defaultSaveDirectory)
        searchBox.setEnabled(self.initState)
        self.queriesLayout.addWidget(searchBox)
        clientLayout.addLayout(self.queriesLayout)

        # Add plus icon
        self.addQuery = PlusIcon('Query', size=20)
        self.addQuery.setEnabled(self.initState)
        clientLayout.addWidget(self.addQuery)

        clientLayout.addStretch(1)
        self.setLayout(self.mainLayout)

        # Connect signals and slots
        self.deleteButton.clicked.connect(self.destroy)
        searchBox.delete.connect(self.updateSearchBoxTitles)
        searchBox.search[str, str, int].connect(self.searchRequest)
        self.addQuery.add.connect(self.addSearchBox)

    def addSearchBox(self):
        self.searchCount += 1
        searchBox = SearchBox(self.maxResults, f'Query #{self.searchCount}', self.defaultSaveDirectory)
        self.queriesLayout.addWidget(searchBox)
        searchBox.delete.connect(self.updateSearchBoxTitles)
        searchBox.search[str, str, int].connect(self.searchRequest)
        self.searchCountUpdated.emit(1, 'added')

    def setDefaultSaveDirectory(self, directory: str):
        self.defaultSaveDirectory = directory
        for s in self.queriesLayout.parentWidget().findChildren(SearchBox):
            s.setSaveDirectory(directory)

    def _clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self._clearLayout(item.layout())

    @pyqtSlot(str, str, int)
    def searchRequest(self, directory:str, query: str, numImages: int):
        if self.client == SupportedSearchClients.GOOGLE_API:
            self.search[str, str, str, str, int].emit(self.apiKey.toPlainText(), self.cseID.toPlainText(), directory, query, numImages)
        elif self.client == SupportedSearchClients.BING_API:
            self.search[str, str, str, int].emit(self.apiKey.toPlainText(), directory, query, numImages)
        elif self.client == SupportedSearchClients.GOOGLE:
            self.search[str, str, int].emit(directory, query, numImages)

    @pyqtSlot()
    def updateSearchBoxEnabledState(self):
        if self.client == SupportedSearchClients.GOOGLE_API:
            # print(len(self.apiKey.toPlainText()), len(self.cseID.toPlainText()))
            state = len(self.apiKey.toPlainText()) == 39 and len(self.cseID.toPlainText()) == 33
        elif self.client == SupportedSearchClients.BING_API:
            state = len(self.apiKey.toPlainText()) == 39

        for s in self.queriesLayout.parentWidget().findChildren(SearchBox):
            s.setEnabled(state)

        self.addQuery.setEnabled(state)

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