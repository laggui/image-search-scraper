import sys
import resources

from PyQt5.QtWidgets import QApplication, QMainWindow, QScrollArea
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QMessageBox
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QFrame, QAction
from PyQt5.QtCore import Qt

from widgets import PlusIcon, SearchClient, ToolBar
from widgets.search_client import SupportedSearchClients
from widgets.utils import newIcon

__appname__ = 'Dataset Builder'

class DatasetBuilderApp(QMainWindow):
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
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        scrollAreaContent = QWidget()
        listLayout = QVBoxLayout()

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

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(scrollAreaContent)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setContentsMargins(0, 0, 0, 0)
        scrollLayout = QVBoxLayout()
        scrollLayout.addWidget(scroll)
        scrollAreaContent.setLayout(listLayout)
        centralWidget.setLayout(scrollLayout)
        centralWidget.layout().setContentsMargins(0, 0, 0, 0)

        # Toolbar
        toolbar = ToolBar()
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Dock widgets

        # Connect signals and slots
        addGoogleAPI.clickableIcon().clicked.connect(lambda state, x=SupportedSearchClients.GOOGLE: self.addSearchClient(x))
        addBingAPI.clickableIcon().clicked.connect(lambda state, x=SupportedSearchClients.BING: self.addSearchClient(x))
        toolbar.actionTriggered[QAction].connect(self.toolButtonPressed)

        # Window settings
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(newIcon('app'))
        self.center()
        self.show()

    # def sendQuery(self)

    def addSearchClient(self, client: SupportedSearchClients):
        self.clientsLayout.addWidget(SearchClient(client))

    def toolButtonPressed(self, button):
        print(f'pressed tool button is {button.text()}')

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