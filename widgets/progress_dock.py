from PyQt5.QtWidgets import QDockWidget, QLabel, QListWidget, QListWidgetItem, QWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from widgets import DownloadProgress

class ProgressDock(QDockWidget):
    """
    Progress dock widget which holds a list of progress items
    """
    _placeholder = 'No download in progress...'
    completed = pyqtSignal(bool)
    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(title, parent)
        self.itemCount = 0
        self.completedCount = 0
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
        self.downloadList.addItem(self._placeholder)

    def addProgressItem(self, title: str):
        # Emit incomplete download signal
        self.completed.emit(False)
        # Remove placeholder text
        if self.itemCount == 0:
            self.downloadList.takeItem(0)
        self.itemCount += 1
        # Create DownloadProgress item
        progress = DownloadProgress(title)
        progress.completed.connect(self.updateCompleteCount)
        # Create QListWidgetItem
        myQListWidgetItem = QListWidgetItem(self.downloadList)
        # Set size hint
        myQListWidgetItem.setSizeHint(progress.sizeHint())
        # Add QListWidgetItem into QListWidget
        self.downloadList.addItem(myQListWidgetItem)
        self.downloadList.setItemWidget(myQListWidgetItem, progress)

    def getItemCount(self):
        return self.itemCount

    @pyqtSlot()
    def removeCompleted(self):
        for idx in reversed(range(self.downloadList.count())):
            listWidgetItem = self.downloadList.item(idx)
            item = self.downloadList.itemWidget(listWidgetItem)
            if isinstance(item, DownloadProgress):
                # remove items only when no search is in progress (disable clear icon, and on the other hand disable search when clear in progress)
                self.itemCount -= 1
                self.completedCount -= 1
                self.downloadList.takeItem(idx)
                item.deleteLater()
                self.completed.emit(False)
        # print(f'Items: {self.itemCount} | Completed: {self.completedCount}')
        self.downloadList.addItem(self._placeholder)

    @pyqtSlot(int, float)
    def setProgressItemValue(self, index: int, value: float):
        # print(f'Setting progress value to {value}')
        listWidgetItem = self.downloadList.item(index)
        item = self.downloadList.itemWidget(listWidgetItem)
        item.setValue(value)

    @pyqtSlot()
    def updateCompleteCount(self):
        self.completedCount += 1
        if self.itemCount == self.completedCount:
            self.completed.emit(True)
        else:
            self.completed.emit(False)