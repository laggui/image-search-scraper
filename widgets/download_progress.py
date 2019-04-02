from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal

from widgets import DeleteButton

class DownloadProgress(QWidget):
    """
    Progress tracker widget
    """
    _min = 0
    _max = 100
    completed = pyqtSignal()
    def __init__(self, text: str, parent: QWidget = None):
        super().__init__(parent)
        vLayout = QVBoxLayout()
        vLayout.setContentsMargins(6, 6, 6, 6)
        textLayout = QHBoxLayout()
        textLayout.addWidget(QLabel(text))
        textLayout.addStretch(1)

        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(20)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setMinimum(self._min)
        self.progressBar.setMaximum(self._max)
        self.progressBar.setValue(self._min)

        vLayout.addLayout(textLayout)
        vLayout.addWidget(self.progressBar)
        self.setLayout(vLayout)

    def setValue(self, value: int):
        self.progressBar.setValue(value)
        if value == self._max:
            self.completed.emit()

    def value(self):
        return self.progressBar.value()