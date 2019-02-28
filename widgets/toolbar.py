from PyQt5.QtWidgets import QToolBar, QWidget, QAction
from PyQt5.QtCore import Qt, pyqtSignal

from widgets.utils import newIcon

class ToolBar(QToolBar):
    """
    ToolBar widget with preset actions defined
    """
    deleteAll = pyqtSignal()
    searchAll = pyqtSignal()
    setDefaultDirectory = pyqtSignal()
    def __init__(self, title: str = 'Global Actions', parent: QWidget = None):
        super().__init__('delete', parent)
        self.setStyleSheet('QToolButton:hover{background: rgba(0, 0, 0, 10%);}')
        # Set default save directory
        setSaveDirAction = QAction(newIcon('folder'), 'Set Default Save Directory For All', self)
        self.addAction(setSaveDirAction)
        self.setSaveDir = self.widgetForAction(setSaveDirAction)

        # Search all queries & download images
        searchAllAction = QAction(newIcon('search-download'), 'Search && Download All', self)
        self.addAction(searchAllAction)
        self.searchAllButton = self.widgetForAction(searchAllAction)

        # Delete all APIs and their corresponding queries
        deleteAllAction = QAction(newIcon('delete'), 'Delete All APIs && Queries', self)
        self.addAction(deleteAllAction)
        self.deleteAllButton = self.widgetForAction(deleteAllAction)

        # Connect signals
        self.setSaveDir.clicked.connect(self.setDefaultDirectory)
        self.searchAllButton.clicked.connect(self.searchAll)
        self.deleteAllButton.clicked.connect(self.deleteAll)

    def setDeleteAllEnabled(self, state):
        self.deleteAllButton.setEnabled(state)

    def setSearchAllEnabled(self, state):
        self.searchAllButton.setEnabled(state)