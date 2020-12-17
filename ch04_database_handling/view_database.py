"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, argparse
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, 
    QHeaderView, QMessageBox)
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel, QSqlTableModel

def parseCommandLine():
    """Use argparse to parse the command line for the SQL data model and any 
    queries to the database. Users can enter multiple queries in the command line."""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data-model", type=str, 
        choices=['read-only', 'read-write'], default="read-only",
        help="Select the type of data model for viewing SQL data: \
            read-only = QSqlQueryModel; read-write = QSqlTableModel")
    parser.add_argument("-q", "--query", type=str, default=["SELECT * FROM customers"], 
        nargs="*", help="Pass a query in the command line")
    args = vars(parser.parse_args())
    return args

class DisplayDatabase(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and its contents."""
        self.setMinimumSize(1000, 500)
        self.setWindowTitle("Ex 4.2 - Display SQL Data in PyQt Tables")

        self.createConnection()
        self.setupTable(args["data_model"], args["query"])
        self.show()
    
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

    def setupTable(self, data_model, query_cmdline):
        """Set up the main window. The SQL model used is based on data_model; 
        The query_cmdline argument is a list of queries from the command line."""
        if data_model == "read-write":
            # Create the model instance
            self.model = QSqlTableModel()
            # Populate the model with data. Example of using setQuery() to display data in the 
            # table view; you would typically use setTable() to populate the model
            for qry in query_cmdline:
                query = QSqlQuery(qry)
                self.model.setQuery(query)
                
        elif data_model == "read-only":
            self.model = QSqlQueryModel()
            # Populate the model with data
            for qry in query_cmdline:
                self.model.setQuery(qry)

        table_view = QTableView()
        table_view.setModel(self.model)
        table_view.hideColumn(0) # Useful if you don't want to view the id values
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setCentralWidget(table_view)

if __name__ == "__main__":
    args = parseCommandLine() # Return any command line arguments
    app = QApplication(sys.argv)
    window = DisplayDatabase()
    sys.exit(app.exec_())