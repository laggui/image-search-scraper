from PyQt5.QtWidgets import QFileDialog, QHBoxLayout, QLabel, QWidget
from PyQt5.QtCore import pyqtSlot

from widgets import ImageButton

class DirectorySelector(QWidget):
    """
    Directory selection widget with folder image button and label on its right to display currently selected directory
    """
    def __init__(self, directory: str, size = 24, parent: QWidget = None):
        super().__init__(parent)
        # Layout
        hLayout = QHBoxLayout()
        dirSelect = ImageButton('folder', size, size)
        dirSelect.setToolTip('Change Save Directory')
        hLayout.addWidget(dirSelect)
        self.directory = QLabel(directory)
        hLayout.addWidget(self.directory)
        hLayout.addStretch(1)
        self.setLayout(hLayout)

        # Connect icon to QFileDialog
        dirSelect.clicked.connect(self.directoryDialog)

    def selectedDirectory(self):
        return self.directory.text()

    def setSelectedDirectory(self, directory: str):
        self.directory.setText(directory)

    @pyqtSlot()
    def directoryDialog(self):
        selected = QFileDialog.getExistingDirectory(self, 'Save images to the directory',
                                                    self.directory.text(), QFileDialog.ShowDirsOnly)
        if selected:
            self.directory.setText(selected)