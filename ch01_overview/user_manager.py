"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, csv
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, 
    QLineEdit, QComboBox, QGroupBox, QTableView, QHeaderView, QHBoxLayout, 
    QFormLayout, QVBoxLayout, QDialog, QFileDialog, QAction)
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtCore import Qt

style_sheet = """
    QGroupBox:title{
        subcontrol-origin: margin;
        padding: 0 10px;
    } """

class UserManager(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setGeometry(100, 100, 500, 300)
        self.setWindowTitle('1.2 - User Manager')

        self.setupModelView()
        self.setupMenu()
        self.show()

    def setupModelView(self):
        """Set up widgets, and standard item model and table view."""
        user_gb = QGroupBox("Users")

        new_user_button = QPushButton(QIcon("images/plus.png"), "Create New User")
        new_user_button.setMaximumWidth(160)
        new_user_button.clicked.connect(self.createNewUserDialog)

        self.list_of_table_headers = ["First Name", "Last Name", "Profile Name", "Location"]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.list_of_table_headers)

        table_view = QTableView()
        table_view.setModel(self.model)
        table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Set initial row and column values
        self.model.setRowCount(0)
        self.model.setColumnCount(4)

        v_box = QVBoxLayout()
        v_box.addWidget(new_user_button, Qt.AlignLeft)
        v_box.addWidget(table_view)

        user_gb.setLayout(v_box)
        self.setCentralWidget(user_gb)

    def setupMenu(self):
        """Set up menu bar."""
        # Create actions for file menu
        save_act = QAction('Save', self)
        save_act.setShortcut('Ctrl+S')
        save_act.triggered.connect(self.saveTableToFile)

        exit_act = QAction('Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(self.close)

        # Create menubar
        menu_bar = self.menuBar()
        # For MacOS users, places menu bar in main window
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(save_act)
        file_menu.addSeparator()
        file_menu.addAction(exit_act)

    def createNewUserDialog(self):
        """Set up the dialog box that allows the user to enter new user information."""
        self.new_user_dialog = QDialog(self)
        self.new_user_dialog.setWindowTitle("Create New User")
        self.new_user_dialog.setModal(True)

        self.enter_first_line = QLineEdit()
        self.enter_last_line = QLineEdit()
        self.display_name_line = QLineEdit()

        locations_list = ["Select Location...", "Algeria", "Argentina", "Bolivia", "Canada", "Denmark",
            "Greece", "Iran", "Liberia", "New Zealand", "Qatar", "Uganda"]

        self.location_cb = QComboBox()
        self.location_cb.addItems(locations_list)

        create_button = QPushButton("Create User")
        create_button.clicked.connect(self.addNewUserToTable)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.new_user_dialog.reject)

        button_h_box = QHBoxLayout()
        button_h_box.addWidget(create_button)
        button_h_box.addSpacing(15)
        button_h_box.addWidget(cancel_button)

        # Add widgets to form layout
        dialog_form = QFormLayout()
        dialog_form.setFormAlignment(Qt.AlignLeft)
        dialog_form.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        dialog_form.addRow("First name", self.enter_first_line)
        dialog_form.addRow("Last name", self.enter_last_line)
        dialog_form.addRow("Display Name", self.display_name_line)
        dialog_form.addRow("Location", self.location_cb)
        dialog_form.addItem(button_h_box)
        
        self.new_user_dialog.setLayout(dialog_form)

        # Restrict the size of the dialog in relation to the size of the 
        # dialog_form's sizeHint()
        self.new_user_dialog.setMaximumSize(dialog_form.sizeHint())
        self.new_user_dialog.show()

    def addNewUserToTable(self):
        """Add information from input widgets in dialog box to a list. If a widget is 
        empty, append None to the list. Finally, add a new row to the table."""
        new_user_info_list = []

        if self.enter_first_line.text() != "":
            new_user_info_list.append(QStandardItem(self.enter_first_line.text()))
        else: 
            new_user_info_list.append(None)
        if self.enter_last_line.text() != "":
            new_user_info_list.append(QStandardItem(self.enter_last_line.text()))
        else: 
            new_user_info_list.append(None)
        if self.display_name_line.text() != "":
            new_user_info_list.append(QStandardItem(self.display_name_line.text()))
        else: 
            new_user_info_list.append(None)
        if self.location_cb.currentIndex() != 0:
            new_user_info_list.append(QStandardItem(self.location_cb.currentText()))
        else: 
            new_user_info_list.append(None)

        # Add a new row to the model
        self.model.appendRow(new_user_info_list)
        self.new_user_dialog.close()

    def saveTableToFile(self):
        """Save user information to a csv file."""
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Table', 
                "", "CSV Files (*.csv)")

        # If file_name exists and there is at least one row in the table, then save
        if file_name and self.model.rowCount() != 0:
            with open(file_name, "w") as csv_wf:
                user_writer = csv.writer(csv_wf, delimiter=',')
                user_writer.writerow(self.list_of_table_headers)
                
                # Iterate through each row and column in the table for row in 
                # range(self.model.rowCount()):
                for row in range(self.model.rowCount()):
                    current_row_list = []
                    for column in range(self.model.columnCount()):
                        item = str(self.model.data(self.model.index(row, column)))
                        current_row_list.append(item)
                    user_writer.writerow(current_row_list)    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = UserManager()
    sys.exit(app.exec_())