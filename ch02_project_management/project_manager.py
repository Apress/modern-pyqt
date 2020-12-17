"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QFrame, 
    QPushButton, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout, QDialog)
from PyQt5.QtCore import Qt, QMimeData, QSize
from PyQt5.QtGui import QDrag, QIcon, QPixmap, QPainter, QTextCursor
from ProjectManagerStyleSheet import style_sheet

class TaskWidget(QFrame):

    def __init__(self, title):
        super().__init__()
        self.setMinimumHeight(32)
        self.setObjectName("Task")
        self.title = title
        self.task_description = ""
    
        task_label = QLabel(title)
        task_label.setObjectName("TaskLabel")
        edit_task_button = QPushButton(QIcon("images/three_dots.png"), None)
        edit_task_button.setIconSize(QSize(28, 28))
        edit_task_button.setMaximumSize(30, 30)
        edit_task_button.clicked.connect(self.specifyTaskInfo)

        task_h_box = QHBoxLayout()
        task_h_box.addWidget(task_label)
        task_h_box.addWidget(edit_task_button)
        self.setLayout(task_h_box)
        
    def specifyTaskInfo(self):
        """Create the dialog box where the user to write more information about 
        their current selected task."""
        self.task_info_dialog = QDialog(self)
        
        task_header = QLabel(self.title)
        task_header.setObjectName("TaskHeader")
        description_label = QLabel("Description")
        description_label.setObjectName("DescriptionLabel")

        self.enter_task_desc_text = QTextEdit()
        self.enter_task_desc_text.setText(self.task_description)
        # The cursor will appear at the end of the text edit input field
        self.enter_task_desc_text.moveCursor(QTextCursor.End)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.confirmTaskDescription)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.task_info_dialog.reject)

        # Create layout for the dialog's buttons
        button_h_box = QHBoxLayout()
        button_h_box.addWidget(save_button)
        button_h_box.addSpacing(15)
        button_h_box.addWidget(cancel_button)

        # Create layout and add widgets for the dialog box
        dialog_v_box = QVBoxLayout()
        dialog_v_box.addWidget(task_header)
        dialog_v_box.addWidget(description_label, Qt.AlignLeft)
        dialog_v_box.addWidget(self.enter_task_desc_text)
        dialog_v_box.addItem(button_h_box)

        self.task_info_dialog.setLayout(dialog_v_box)
        self.task_info_dialog.show() # Display dialog box

    def confirmTaskDescription(self):
        """When user selects Save, save the info written in the text 
        edit widget in the task_description variable."""
        text = self.enter_task_desc_text.toPlainText()
        
        if text == "":
            pass
        elif text != "":
            self.task_description = text

        self.task_info_dialog.close() # Close dialog box

    def mousePressEvent(self, event):
        """Reimplement what happens when the user clicks on the widget."""
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        """Reimplement how to handle the widget being dragged. Change the mouse 
        icon when the user begins dragging the object."""
        drag = QDrag(self)
        # When the user begins dragging the object, change the cursor's icon 
        # and set the drop action
        drag.setDragCursor(QPixmap("images/drag.png"), Qt.MoveAction)
        mime_data = QMimeData()
        drag.setMimeData(mime_data)

        # Create the QPainter object that will draw the widget being dragged 
        pixmap = QPixmap(self.size()) # Get the size of the object
        painter = QPainter(pixmap) # Set the painter’s pixmap
        # Draw the pixmap; grab() renders the widget into a pixmap specified by rect()
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()

        drag.setPixmap(pixmap) # Set the pixmap to represent the drag action
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.MoveAction)

class TaskContainer(QWidget):

    def __init__(self, title, bg_color):
        super().__init__()
        self.setAcceptDrops(True)
        self.setObjectName("ContainerWidget")

        container_label = QLabel(title) # Container's title
        # Set the background color of the container's label
        container_label.setStyleSheet("background-color: {}".format(bg_color))
        container_frame = QFrame() # Main container to hold all TaskWidget objects
        container_frame.setObjectName("ContainerFrame")

        self.new_task_button = QPushButton("+ Add a new task")
        self.new_task_button.clicked.connect(self.createNewTask)

        self.tasks_v_box = QVBoxLayout()
        self.tasks_v_box.insertWidget(-1, self.new_task_button)
        container_frame.setLayout(self.tasks_v_box)

        # Main layout for container class
        container_v_box = QVBoxLayout()
        container_v_box.setSpacing(0) # No space between widgets
        container_v_box.setAlignment(Qt.AlignTop)
        container_v_box.addWidget(container_label)
        container_v_box.addWidget(container_frame)
        container_v_box.setContentsMargins(0, 0, 0, 0)

        self.setLayout(container_v_box)

    def createNewTask(self):
        """Set up the dialog box that allows the user to create a new task."""
        self.new_task_dialog = QDialog(self)
        self.new_task_dialog.setWindowTitle("Create New Task")
        self.new_task_dialog.setModal(True) # Create a modal dialog

        self.enter_task_line = QLineEdit()
        self.enter_task_line.setPlaceholderText("Enter a title for this task...")

        self.add_task_button = QPushButton("Add Task")
        self.add_task_button.clicked.connect(self.confirmTask)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.new_task_dialog.reject)
        
        # Create layout for the dialog's buttons
        button_h_box = QHBoxLayout()
        button_h_box.addWidget(self.add_task_button)
        button_h_box.addSpacing(15)
        button_h_box.addWidget(cancel_button)

        # Create layout and add widgets for the dialog box
        dialog_v_box = QVBoxLayout()
        dialog_v_box.addWidget(self.enter_task_line)
        dialog_v_box.addItem(button_h_box)

        self.new_task_dialog.setLayout(dialog_v_box)
        self.new_task_dialog.show()

    def confirmTask(self):
        """If user clicks Add Task in dialog box, create new TaskWidget
        object and insert it into the container's layout."""
        if self.enter_task_line.text() != "":
            new_task = TaskWidget(self.enter_task_line.text())
            self.tasks_v_box.insertWidget(0, new_task, 0)
        self.new_task_dialog.close()

    def dragEnterEvent(self, event):
        """Accept the dragging event onto the widget."""
        event.setAccepted(True)

    def dropEvent(self, event):
        """Check the source of the mouse event. If the source does not 
        already exist in the target widget then the drop is allowed."""
        event.setDropAction(Qt.MoveAction)
        source = event.source()

        if source not in self.children():
            event.setAccepted(True)
            self.tasks_v_box.addWidget(source)
        else:
            event.setAccepted(False)

        # Whenever a widget is dropped, ensure new_task_button stays 
        # at the bottom of the container
        self.tasks_v_box.insertWidget(-1, self.new_task_button)

class ProjectManager(QWidget):
    
    def __init__(self):
        super().__init__() 
        self.initializeUI() 

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setMinimumSize(800, 400)
        self.showMaximized()
        self.setWindowTitle('2.1 - Project Manager')

        self.setupWidgets()
        self.show()

    def setupWidgets(self):
        """Set up the containers and main layout for the window."""
        possible_container = TaskContainer("Possible Projects", "#0AC2E4") # Blue
        progress_container = TaskContainer("In Progress", "#F88A20") # Orange
        review_container = TaskContainer("Under Review", "#E7CA5F") # Yellow
        completed_container = TaskContainer("Completed Projects", "#10C94E") # Green

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(possible_container)
        main_h_box.addWidget(progress_container)
        main_h_box.addWidget(review_container)
        main_h_box.addWidget(completed_container)

        self.setLayout(main_h_box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = ProjectManager()
    sys.exit(app.exec_())