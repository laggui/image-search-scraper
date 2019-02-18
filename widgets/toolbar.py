from PyQt5.QtWidgets import QToolBar, QWidget, QAction
from PyQt5.QtCore import Qt

from widgets.utils import newIcon

class ToolBar(QToolBar):
    def __init__(self, title: str = 'Global Actions', parent: QWidget = None):
        super().__init__('delete', parent)
        self.setStyleSheet('QToolButton:hover{background: rgba(0, 0, 0, 10%);}')
        setSaveDirAll = QAction(newIcon('folder'), 'Set Default Save Directory', self)
        self.addAction(setSaveDirAll)
        searchAll = QAction(newIcon('search-download'), 'Search && Download All', self)
        self.addAction(searchAll)
        deleteAll = QAction(newIcon('delete'), 'Delete All APIs && Queries', self)
        self.addAction(deleteAll)