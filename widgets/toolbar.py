from PyQt5.QtWidgets import QToolBar, QWidget, QAction
from PyQt5.QtCore import Qt

from widgets.utils import newIcon

class ToolBar(QToolBar):
    """
    ToolBar widget with preset actions defined
    """
    def __init__(self, title: str = 'Global Actions', parent: QWidget = None):
        super().__init__('delete', parent)
        self.setStyleSheet('QToolButton:hover{background: rgba(0, 0, 0, 10%);}')
        # Set default save directory
        setSaveDirAction = QAction(newIcon('folder'), 'Set Default Save Directory', self)
        self.addAction(setSaveDirAction)
        self.setSaveDir = self.widgetForAction(setSaveDirAction)

        # Search all queries & download images
        searchAllAction = QAction(newIcon('search-download'), 'Search && Download All', self)
        self.addAction(searchAllAction)
        self.searchAll = self.widgetForAction(searchAllAction)

        # Delete all APIs and their corresponding queries
        deleteAllAction = QAction(newIcon('delete'), 'Delete All APIs && Queries', self)
        self.addAction(deleteAllAction)
        self.deleteAll = self.widgetForAction(deleteAllAction)

    def setSaveDirButton(self):
        """Returns the toolbar button in order to access its clicked signal externally"""
        return self.setSaveDir

    def searchAllButton(self):
        """Returns the toolbar button in order to access its clicked signal externally"""
        return self.searchAll

    def deleteAllButton(self):
        """Returns the toolbar button in order to access its clicked signal externally"""
        return self.deleteAll