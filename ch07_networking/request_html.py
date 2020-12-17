"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSplitter, 
    QTextEdit, QToolBar, QHBoxLayout, QAction)
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QFont, QIcon

class DisplayWebContent(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.showMaximized() # Window starts maximized
        self.setMinimumSize(1000, 500)
        self.setWindowTitle('Ex 7.1 - Request HTML')

        self.setupWindow()
        self.setupToolbar()
        self.show()

    def setupWindow(self):
        """Set up the widgets in the main window."""
        home_page_url = "https://www.google.com"

        # Create the view instance for the web browser
        self.web_view = QWebEngineView()
        self.web_view.setUrl(QUrl(home_page_url))
        self.web_view.urlChanged.connect(self.loadHTML)

        self.html_text_edit = QTextEdit()
        self.html_text_edit.setText("Loading HTML...")
        self.html_text_edit.setFont(QFont('Courier', 12))

        # Create splitter container and arrange widgets
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.web_view)
        splitter.addWidget(self.html_text_edit)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(splitter)

        main_container = QWidget()
        main_container.setLayout(main_h_box)
        self.setCentralWidget(main_container)

    def setupToolbar(self):
        """Create the toolbar for navigating web pages."""
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Create actions
        back_act = QAction(QIcon("icons/back.png"), "Back Button", toolbar)
        back_act.triggered.connect(self.web_view.back)

        forward_act = QAction(QIcon("icons/forward.png"), "Forward Button", toolbar)
        forward_act.triggered.connect(self.web_view.forward)

        # Add actions to the toolbar
        toolbar.addAction(back_act)
        toolbar.addAction(forward_act)

    def loadHTML(self):
        """Send a GET request to retrieve the current web page and its data."""
        # Retrieve the url of the current page
        url = self.web_view.url()

        request = QNetworkRequest(QUrl(url))

        # Create QNetworkAccessManager to send request; emit finsihed() signal 
        # to connect to replyFinished() and display the page's HTML
        self.manager = QNetworkAccessManager()
        self.manager.finished.connect(self.replyFinished)
        self.manager.get(request)

    def replyFinished(self, reply):
        """Get the reply data. Check for any errors that occurred while loading
        the web pages."""
        error = reply.error()

        if error == QNetworkReply.NoError:
            # The function readAll() returns a byte array containing 
            # the requested data
            data = reply.readAll()

            # Use BeautifulSoup to "prettify" the HTML before displaying it
            soup = BeautifulSoup(data, features="html5lib")
            beautified_html = soup.prettify()
            self.html_text_edit.setPlainText(beautified_html)
        else:
            error = "[INFO] Error: {}".format(str(error))
            self.html_text_edit.setPlainText(error + "\n" + reply.errorString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DisplayWebContent()
    sys.exit(app.exec_())