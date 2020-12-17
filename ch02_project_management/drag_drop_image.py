"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QFileDialog)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

style_sheet = """
    QLabel#TargetLabel{
        color: darkgrey;
        border: 2px dashed darkgrey;
        font: 24px 'Helvetica';
        qproperty-alignment: AlignCenter
    }

    QLabel{
        color: darkgrey;
        font: 18px 'Helvetica';
        qproperty-alignment: AlignCenter
    }

    QPushButton{
        border: 1px solid;
        border-radius: 3px;
        font: 18px 'Helvetica'
    }

    QPushButton:pressed{
        background-color: skyblue
    }"""

class TargetLabel(QLabel):
    
    def __init__(self):
        super().__init__()
        
        # Create interface and layout
        self.setText("Drag & Drop Files Here")
        self.setObjectName("TargetLabel")

        self.or_label = QLabel("or")
        self.select_image_button = QPushButton("Select Files")
        self.select_image_button.setFixedSize(150, 50)
        self.select_image_button.clicked.connect(self.selectImageFile)
        
        label_v_box = QVBoxLayout()
        label_v_box.addStretch(3)
        label_v_box.addWidget(self.or_label)
        label_v_box.addWidget(self.select_image_button, 0, Qt.AlignCenter)
        label_v_box.addStretch(1)

        self.setLayout(label_v_box)

    def setPixmap(self, image):
        """Reimplement setPixmap() method so that image will appear on objects 
        created from TargetLabel class. Hide other widgets."""
        # Method gets called on parent class. Otherwise, the image would not be seen.
        super().setPixmap(image)

        self.or_label.setVisible(False)
        self.select_image_button.setVisible(False)

    def selectImageFile(self):
        """Open an image file and display it on the label widget."""
        image_file, _ = QFileDialog.getOpenFileName(self, "Open Image", "",
            "JPG Files (*.jpeg *.jpg );;PNG Files (*.png);;Bitmap Files(*.bmp);;\
            GIF Files (*.gif)")

        if image_file:
            self.setPixmap(QPixmap(image_file))
            self.setScaledContents(True)

class DropTargetEx(QWidget):

    def __init__(self):
        super().__init__() 
        self.initializeUI() 

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Ex 2.1 - Drag and Drop Image")
        self.setAcceptDrops(True)

        self.setupWidgets()
        self.show()

    def setupWidgets(self):
        """Set up the label widget that will act as the target for the 
        image drop, and the main layout."""
        self.target_label = TargetLabel()

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(self.target_label)

        self.setLayout(main_v_box)

    def dragEnterEvent(self, event):
        """Reimplement event handler to check the data type of item 
        being dragged onto the widget."""
        if event.mimeData().hasImage:
            event.setAccepted(True)
        else:
            event.setAccepted(False)

    def dropEvent(self, event):
        """Reimplement event handler to handle when an item is dropped
        on the target. If the mimeData is an image, then the item is accepted."""
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            image_path = event.mimeData().urls()[0].toLocalFile()
            self.setImage(image_path)

            event.setAccepted(True)
        else:
            event.setAccepted(False)

    def setImage(self, image_file):
        """Set the target's pixmap when an item is dropped onto the label area."""
        self.target_label.setPixmap(QPixmap(image_file))
        self.target_label.setScaledContents(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = DropTargetEx()
    sys.exit(app.exec_())