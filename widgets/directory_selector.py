from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSlot
from pathlib import Path

from widgets import ImageButton

class DirectorySelector(QWidget):
    """
    Directory selection widget with folder image button and label on its right to display currently selected directory
    """
    def __init__(self, size = 24, parent: QWidget = None):
        super().__init__(parent)
        # Layout
        hLayout = QHBoxLayout()
        dirSelect = ImageButton('folder', size)
        hLayout.addWidget(dirSelect)
        self.directory = QLabel(str(Path.home()))
        hLayout.addWidget(self.directory)
        hLayout.addStretch(1)
        self.setLayout(hLayout)

        # Connect icon to QFileDialog
        dirSelect.clicked.connect(self.directoryDialog)

    def selectedDirectory(self):
        return self.directory.text()

    @pyqtSlot()
    def directoryDialog(self):
        selected = QFileDialog.getExistingDirectory(self, 'Save images to the directory',
                                                    self.directory.text(), QFileDialog.ShowDirsOnly)
        if selected:
            self.directory.setText(selected)