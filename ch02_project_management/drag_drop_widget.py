"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QFrame)
from PyQt5.QtGui import QDrag
from PyQt5.QtCore import Qt, QMimeData

style_sheet = """
    QFrame#Containers{
        background-color: lightgrey;
        border: 2px solid black
    }"""

# Class for objects that can be dragged
class DragButton(QPushButton):
    
    def __init__(self, text):
        super().__init__(text)
        self.setText(text)

    def mousePressEvent(self, event):
        """Reimplement the event handler when the object is clicked on."""
        if event.button() == Qt.LeftButton:
            self.drag_start_postion = event.pos()      

    def mouseMoveEvent(self, event):
        """Reimplement the event handler when the object is being dragged."""
        drag = QDrag(self) # Create drag object for MIME-based drag and drop
        mime_data = QMimeData()

        drag.setMimeData(mime_data)
        # Begins the drag and drop operation and sets the type of drop action
        drag.exec_(Qt.MoveAction) 

# Target: Where the dragged object is being dragged
class DropTargetWidget(QFrame):
    
    def __init__(self):
        super().__init__()
        # Enable drop events 
        self.setAcceptDrops(True)
        self.setObjectName("Containers")

        # Create drop target class layout
        self.container_v_box = QVBoxLayout()
        self.container_v_box.setAlignment(Qt.AlignTop)
        self.setLayout(self.container_v_box)

    def addButton(self, button):
        """Add QPushButton widgets to container class layout."""
        self.container_v_box.addWidget(button, 0, Qt.AlignCenter)
    
    def dragEnterEvent(self, event):
        """Accept drops when objects are dragged inside widget."""
        event.acceptProposedAction()

    def dropEvent(self, event):
        """Check the source of the mouse event. If the source (widget) does not
        already exist in the target widget then it can be dropped."""
        event.setDropAction(Qt.MoveAction)
        source = event.source() # Source of the mouse event

        if source not in self.children():
            event.setAccepted(True)
            self.container_v_box.addWidget(source, 0, Qt.AlignCenter)
        else:
            event.setAccepted(False)

class DragDropWidgetsEx(QWidget):

    def __init__(self):
        super().__init__() 
        self.initializeUI() 

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Ex 2.2 - Drag and Drop Widgets")

        self.setupWidgets()
        self.show()

    def setupWidgets(self):
        """Set up the left and right DropTargetWidget objects, add a single 
        DragButton object to each one, and create the main layout for the GUI."""
        left_target = DropTargetWidget()
        left_label = DragButton("Left")
        left_target.addButton(left_label)

        right_target = DropTargetWidget()
        right_label = DragButton("Right")
        right_target.addButton(right_label)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(left_target)
        main_h_box.addWidget(right_target)

        self.setLayout(main_h_box)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = DragDropWidgetsEx()
    sys.exit(app.exec_())