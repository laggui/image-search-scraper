import sys
import resources
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QAction, QFileDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

from widgets import ImageButton, PlusIcon, ProgressDock, SearchClient, SearchTask, ToolBar
from widgets.utils import newIcon, reduceString

from webscraper import SupportedSearchClients

__appname__ = 'Image Search Scraper'

class ImageSearchScraperApp(QMainWindow):
    searchCountUpdated = pyqtSignal()
    clientCountUpdated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.title = __appname__
        self.left = 100
        self.top = 100
        self.width = 1024
        self.height = 768
        self.defaultSaveDir = str(Path.home()).replace('\\', '/')
        self.searchCount = 0
        self.clientCount = 0
        self.initUI()

    def initUI(self):
        # Main layout
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        scrollAreaContent = QWidget()
        listLayout = QVBoxLayout()

        # Search Clients layout
        self.clientsLayout = QVBoxLayout()
        firstSearchClient = SearchClient(SupportedSearchClients.GOOGLE_API, self.defaultSaveDir)
        self.clientsLayout.addWidget(firstSearchClient)
        self.clientCount = 1 # update client count
        self.searchCount = 1
        listLayout.addLayout(self.clientsLayout)

        # Layout to add additional API search clients
        apiPlusLayout = QHBoxLayout()
        apiPlusLayout.setAlignment(Qt.AlignRight)
        addGoogleAPI = ImageButton('add-google-api', 49, 32)
        addGoogleAPI.setToolTip('Add Google Custom Search Engine API Instance')
        apiPlusLayout.addWidget(addGoogleAPI)
        addBingAPI = ImageButton('add-bing-api', 49, 32)
        addBingAPI.setToolTip('Add Bing Image Search API Instance')
        apiPlusLayout.addWidget(addBingAPI)
        addGoogleScraper = ImageButton('add-google-scraper', 49, 32)
        addGoogleScraper.setToolTip('Add Google Image Scraper Instance')
        apiPlusLayout.addWidget(addGoogleScraper)
        # apiPlusLayout.addStretch(1)
        listLayout.addLayout(apiPlusLayout)

        listLayout.addStretch(1)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(scrollAreaContent)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setContentsMargins(0, 0, 0, 0)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setMinimumWidth(250)
        scrollLayout = QVBoxLayout()
        scrollLayout.addWidget(scroll)
        scrollAreaContent.setLayout(listLayout)
        centralWidget.setLayout(scrollLayout)
        centralWidget.layout().setContentsMargins(0, 0, 0, 0)

        # Toolbar
        self.toolbar = ToolBar()
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        # Dock widgets
        self.downloadProgressDock = ProgressDock('Queries Download Progress')
        self.addDockWidget(Qt.RightDockWidgetArea, self.downloadProgressDock)

        # Connect signals and slots
        addGoogleScraper.clicked.connect(lambda state, x=SupportedSearchClients.GOOGLE: self.addSearchClient(x))
        self.searchCountUpdated.connect(self.updateToolbar)
        self.clientCountUpdated.connect(self.updateToolbar)
        addGoogleAPI.clicked.connect(lambda state, x=SupportedSearchClients.GOOGLE_API: self.addSearchClient(x))
        addBingAPI.clicked.connect(lambda state, x=SupportedSearchClients.BING_API: self.addSearchClient(x))
        self.toolbar.setDefaultDirectory.connect(self.setDefaultSaveDirectory)
        # self.toolbar.searchAll.connect(self.searchAllQueries)
        self.toolbar.deleteAll.connect(self.removeAllSearchClients)
        firstSearchClient.delete.connect(self.updateClientCount)
        firstSearchClient.search[str, str, str, str, int].connect(self.startGoogleAPISearchTask)
        firstSearchClient.searchCountUpdated[int, str].connect(self.updateSearchCount)

        # Window settings
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(newIcon('app'))
        self.center()
        self.show()

    @pyqtSlot(str, str, int)
    def startGoogleSearchTask(self, directory: str, query: str, numImages: int):
        """
        Start Google Image Scraper search task
        """
        directory = directory + '/Google_API'
        self.downloadProgressDock.addProgressItem(reduceString(directory + '/' + query))
        idx = self.downloadProgressDock.getItemCount() - 1
        self.thread = QThread(self)
        self.searchTask = SearchTask(idx, SupportedSearchClients.GOOGLE, directory, query, numImages)
        self.searchTask.moveToThread(self.thread)
        self.searchTask.finished.connect(self.thread.terminate)
        self.searchTask.updateProgress[int, float].connect(self.downloadProgressDock.setProgressItemValue)
        self.thread.started.connect(self.searchTask.executeSearchTask)
        self.thread.start()
        

    @pyqtSlot(str, str, str, int)
    def startBingAPISearchTask(self, apiKey: str, directory: str, query: str, numImages: int):
        """
        Start Bing Image Search API search task
        """
        print('Start Bing Image Search API search task')

    @pyqtSlot(str, str, str, str, int)
    def startGoogleAPISearchTask(self, apiKey: str, cseID: str, directory: str, query: str, numImages: int):
        """
        Start Google Custom Search JSON API search task
        """
        print('Start Google Custom Search JSON API search task')

    @pyqtSlot()
    def updateToolbar(self):
        self.toolbar.setSearchAllEnabled(self.searchCount > 0)
        self.toolbar.setDeleteAllEnabled(self.clientCount > 0)

    @pyqtSlot()
    def setDefaultSaveDirectory(self):
        selected = QFileDialog.getExistingDirectory(self, 'Save images to the directory',
                                                    self.defaultSaveDir, QFileDialog.ShowDirsOnly)
        if selected:
            self.defaultSaveDir = selected
            for s in self.clientsLayout.parentWidget().findChildren(SearchClient):
                s.setDefaultSaveDirectory(self.defaultSaveDir)
                # print('Changed default save directory')

    @pyqtSlot()
    def removeAllSearchClients(self):
        mboxtitle = 'Delete All'
        mboxmsg = 'Are you sure you want to delete all search client instances and their corresponding queries?'
        reply = QMessageBox.warning(self, mboxtitle, mboxmsg,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            for s in self.clientsLayout.parentWidget().findChildren(SearchClient):
                s.destroy()

    @pyqtSlot(SupportedSearchClients)
    def addSearchClient(self, client: SupportedSearchClients):
        self.clientCount += 1
        self.searchCount += 1
        clientWidget = SearchClient(client, self.defaultSaveDir)
        self.clientsLayout.addWidget(clientWidget)
        clientWidget.delete.connect(self.updateClientCount)
        clientWidget.searchCountUpdated[int, str].connect(self.updateSearchCount)
        if client == SupportedSearchClients.GOOGLE_API:
            clientWidget.search[str, str, str, str, int].connect(self.startGoogleAPISearchTask)
        elif client == SupportedSearchClients.BING_API:
            clientWidget.search[str, str, str, int].connect(self.startBingAPISearchTask)
        elif client == SupportedSearchClients.GOOGLE:
            clientWidget.search[str, str, int].connect(self.startGoogleSearchTask)
        self.clientCountUpdated.emit()

    @pyqtSlot()
    def updateClientCount(self):
        self.clientCount -= 1
        # print(f'Client count: {self.clientCount}')
        self.clientCountUpdated.emit()

    @pyqtSlot(int, str)
    def updateSearchCount(self, count: int, action: str):
        if action == 'added':
            self.searchCount += count
        elif action == 'removed':
            self.searchCount -= count
        # print(f'Search count: {self.searchCount} ({action} {count})')
        self.searchCountUpdated.emit()

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def closeEvent(self, event):
        mboxtitle = 'Exit'
        mboxmsg = 'Are you sure you want to quit?'
        reply = QMessageBox.warning(self, mboxtitle, mboxmsg,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = ImageSearchScraperApp()
    sys.exit(app.exec_())