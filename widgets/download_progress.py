from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt, pyqtSlot

class DownloadProgress(QWidget):
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
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        # print(f'Progress value: {self.progressBar.value()}')

        vLayout.addLayout(textLayout)
        vLayout.addWidget(self.progressBar)
        self.setLayout(vLayout)

    def setValue(self, value: int):
        self.progressBar.setValue(value)

    def value(self):
        return self.progressBar.value()