from PyQt5.QtWidgets import QDockWidget, QLabel, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtCore import pyqtSlot

from widgets import DownloadProgress

class ProgressDock(QDockWidget):
    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(title, parent)
        self.itemCount = 0
        # Widget initialization
        self.setContentsMargins(0, 0, 11, 11)
        self.setFixedWidth(200)
        self.setTitleBarWidget(QLabel()) # empty title label
        self.setFloating(True)

        # List of queries that are being tracked for download progress
        self.downloadList = QListWidget(self)
        self.downloadList.setStyleSheet('QListWidget{border: 1px solid lightgray; background: white;}\
                                        QListWidget:item{color: lightgray;} QListWidget:item:hover{background: transparent;}')
        self.setWidget(self.downloadList)

        # Placeholder text
        self.downloadList.addItem('No images set to download...')

    def addProgressItem(self, title: str):
        # Remove placeholder text
        if self.itemCount == 0:
            self.downloadList.takeItem(0)
        self.itemCount += 1
        # Create DownloadProgress item
        progress = DownloadProgress(title)
        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(self.downloadList)
        # Set size hint
        myQListWidgetItem.setSizeHint(progress.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.downloadList.addItem(myQListWidgetItem)
        self.downloadList.setItemWidget(myQListWidgetItem, progress)
        # 'query_id': str(0), 'client_type': 'google', 'query': 'apples', 'num_images': 66
        # C:/Users/guila/Downloads/data/Google_API/apples

    @pyqtSlot(int, float)
    def setProgressItemValue(self, index: int, value: float):
        # print(f'Setting progress value to {value}')
        listWidgetItem = self.downloadList.item(index)
        item = self.downloadList.itemWidget(listWidgetItem)
        item.setValue(value)

    def getItemCount(self):
        return self.itemCount