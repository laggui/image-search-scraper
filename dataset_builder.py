import sys
import resources

from PyQt5.QtWidgets import QApplication, QScrollArea
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

from widgets import PlusIcon, SearchClient
from widgets.search_client import SupportedSearchClients
from widgets.utils import newIcon

__appname__ = 'Dataset Builder'

class DatasetBuilderApp(QScrollArea):
    def __init__(self):
        super().__init__()
        self.title = __appname__
        self.left = 100
        self.top = 100
        self.width = 800
        self.height = 640
        self.initUI()

    def initUI(self):
        # Main layout
        centralWidget = QWidget()
        listLayout = QVBoxLayout(centralWidget)

        # Search Clients layout
        self.clientsLayout = QVBoxLayout()
        self.clientsLayout.addWidget(SearchClient(SupportedSearchClients.GOOGLE))
        listLayout.addLayout(self.clientsLayout)

        # Layout to add additional API search clients
        apiPlusLayout = QHBoxLayout()
        addGoogleAPI = PlusIcon('Google')
        apiPlusLayout.addWidget(addGoogleAPI)
        addBingAPI = PlusIcon('Bing')
        apiPlusLayout.addWidget(addBingAPI)
        apiPlusLayout.addStretch(1)
        listLayout.addLayout(apiPlusLayout)

        listLayout.addStretch(1)

        # Connect signals and slots
        addGoogleAPI.clickableIcon().clicked.connect(lambda x=SupportedSearchClients.GOOGLE: self.addSearchClient(x))
        addBingAPI.clickableIcon().clicked.connect(lambda x=SupportedSearchClients.BING: self.addSearchClient(x))

        self.setWidget(centralWidget)
        self.setWidgetResizable(True)

        # Window settings
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(newIcon('app'))
        self.center()
        self.show()

    def addSearchClient(self, client: SupportedSearchClients):
        self.clientsLayout.addWidget(SearchClient(client))

    def center(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

    def closeEvent(self, event):
        mboxtitle = 'Exit'
        mboxmsg = 'Are you sure you want to quit?'
        reply = QMessageBox.warning(self, mboxtitle, mboxmsg,
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
            self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = DatasetBuilderApp()
    sys.exit(app.exec_())