"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QTextEdit, QTableView, 
    QTreeView, QHeaderView, QSplitter, QToolBar, QAction, QFileSystemModel, QMessageBox, 
    QHBoxLayout, QSplashScreen)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QDir
from Login import LoginGUI # Import the login script

class SQLManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and its contents."""
        self.setMinimumSize(1100, 800)
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())
        self.setWindowTitle("4.1 - SQL Management GUI")

        self.login = LoginGUI(self)
        self.login.show()

        self.createConnection()
        self.setupWindow()
        self.setupToolbar()

    def createConnection(self):
        """Set up connection to the database. Check if the tables needed exist."""
        self.database = QSqlDatabase.addDatabase("QSQLITE")
        self.database.setDatabaseName("databases/FishingStores.sql")

        if not self.database.open():
            print("Unable to open data source file.")
            print("Connection failed: ", self.database.lastError().text())
            sys.exit(1) # Error code 1 - signifies error in opening file
    
        # Check if the tables we want to use exist in the database
        tables_needed = {'customers', 'stores', 'orders', 'products', 'order_products'}
        tables_not_found = tables_needed - set(self.database.tables())
        if tables_not_found:
            QMessageBox.critical(None, 'Error',
                'The following tables are missing from the database: {}'.format(tables_not_found))
            sys.exit(1) # Error code 1 – signifies error

    def setupWindow(self):
        """Set up the directory model/view instances, SQL model/view instances, and 
        other widgets to be displayed in the main window."""
        # Create tree model/view for displaying databases in the directory
        directory = QDir.currentPath() + "/databases"

        system_model = QFileSystemModel()
        system_model.setRootPath(directory)
        index = system_model.index(directory)

        tree_view = QTreeView()
        tree_view.setIndentation(15) # Indentation of items in view
        tree_view.setMaximumWidth(300)
        tree_view.setModel(system_model)
        tree_view.setRootIndex(index)

        self.query_entry_field = QTextEdit()
        self.query_entry_field.setFont(QFont("Courier", 14))
        self.query_entry_field.setPlaceholderText("Enter your queries here...")

        # Create the model/view instances 
        self.sql_model = QSqlQueryModel()

        # Create the table view instance and set its parameters and its delegate
        table_view = QTableView()
        table_view.setAlternatingRowColors(True)
        table_view.setModel(self.sql_model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Create splitter that contains the text edit and table view objects
        splitter = QSplitter()
        splitter.setOrientation(Qt.Vertical)
        splitter.addWidget(self.query_entry_field)
        splitter.addWidget(table_view)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(tree_view)
        main_h_box.addWidget(splitter)

        main_container = QWidget()
        main_container.setLayout(main_h_box)
        self.setCentralWidget(main_container)

    def setupToolbar(self):
        """Create the toolbar for running queries and clearing the text edit widget."""
        toolbar = QToolBar(self)
        toolbar.setIconSize(QSize(24, 24))
        self.addToolBar(Qt.RightToolBarArea, toolbar)

        # Create actions 
        clear_text_act = QAction(QIcon("icons/clear.png"), "Clear Query", toolbar)
        clear_text_act.setToolTip("Clear the queries in the text field.")
        clear_text_act.triggered.connect(self.clearText)

        run_query_act = QAction(QIcon("icons/run.png"), "Run Query", toolbar)
        run_query_act.setToolTip("Run the queries in the text field.")
        run_query_act.triggered.connect(self.runQuery)

        # Add actions to the toolbar 
        toolbar.addAction(clear_text_act)
        toolbar.addAction(run_query_act)

    def runQuery(self):
        """Run the query/queries entered in the QTextEdit widget."""
        query_text = self.query_entry_field.toPlainText()
        queries = query_text.split('\n')

        if query_text != "":
            for qry in queries:
                if qry == "":
                    # Pass over empty lines
                    pass
                else:
                    query = QSqlQuery(qry)
                    self.sql_model.setQuery(query)
        
    def clearText(self):
        """Clear the QTextEdit widget's text."""
        self.query_entry_field.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Display splash screen
    splash = QSplashScreen(QPixmap("images/sql_splashscreen.png"))
    splash.show()
    app.processEvents()

    window = SQLManager()
    splash.finish(window)

    sys.exit(app.exec_())