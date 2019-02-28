from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread

from webscraper import BingImageSearchClient, GoogleImageScraper, GoogleCustomSearchEngineClient
from webscraper import SupportedSearchClients, download_all_images

class SearchTask(QObject):
    updateProgress = pyqtSignal(int, float)
    finished = pyqtSignal()
    def __init__(self, idx: int, client: SupportedSearchClients, directory: str, query: str, numImages: int,
                 startIdx: int = 0, apiKey: str = None, cseID: str = None, parent: QObject = None):
        super().__init__(parent)
        self.idx = idx
        self.client = client
        self.directory = directory
        self.query = query
        self.numImages = numImages
        self.startIdx = startIdx
        self.apiKey = apiKey
        self.cseID = cseID

    @pyqtSlot()
    def executeSearchTask(self):
        if self.client == SupportedSearchClients.GOOGLE:
            client = GoogleImageScraper()
        elif self.client == SupportedSearchClients.GOOGLE_API:
            client = GoogleCustomSearchEngineClient(self.cseID, self.apiKey)
        elif self.client == SupportedSearchClients.BING_API:
            client = BingImageSearchClient(self.apiKey)
        links = client.get_links(self.query, self.numImages, self.startIdx)
        download_all_images(self.query, self.directory, links, query_id=self.idx, progress_object=self)
        self.finished.emit()