"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, os, cv2, time
from numpy import ndarray
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QLineEdit, QFrame, QFileDialog, QMessageBox, QHBoxLayout, 
    QVBoxLayout, QAction)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal

style_sheet = """
    QLabel#VideoLabel{
        color: darkgrey;
        border: 2px solid darkgrey;
        qproperty-alignment: AlignCenter
    }"""

class VideoWorkerThread(QThread):
    """Worker thread for capturing video and for performing human detection."""
    frame_data_updated = pyqtSignal(ndarray)
    invalid_video_file = pyqtSignal()

    def __init__(self, parent, video_file=None):
        super().__init__() 
        self.parent = parent
        self.video_file = video_file

    def run(self):
        """The code that we want to run in a separate thread, in this case
        capturing video using OpenCV, is placed in this function. run() is called
        after start()."""
        capture = cv2.VideoCapture(self.video_file) # 0 opens the default camera

        if not capture.isOpened():
            self.invalid_video_file.emit()
        else:
            while self.parent.thread_is_running:
                # Read frames from the camera
                ret_val, frame = capture.read()
                if not ret_val:
                    break # Error or reached the end of the video
                else: 
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    self.frame_data_updated.emit(frame)
                    # waitKey() displays the image for a specified time, in this case 30 ms.
                    # On platforms, such as Linux, using waitKey() will cause errors. To avoid
                    # problems, use sleep() to pause between frames. You can experiment with 
                    # the functions or values to adapt to the speed/quality of your video
                    #cv2.waitKey(30)
                    time.sleep(0.03)

    def stopThread(self):
        """Process all pending events before stopping the thread."""
        self.wait()
        QApplication.processEvents()  

class DisplayVideo(QMainWindow):

    def __init__(self):
        super().__init__() 
        self.initializeUI() 

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setMinimumSize(800, 500)
        self.setWindowTitle('Ex 5.2 - Displaying Videos')
        
        self.thread_is_running = False

        self.setupWindow()
        self.setupMenu()
        self.show()

    def setupWindow(self):
        """Set up widgets in the main window."""
        self.video_display_label = QLabel()
        self.video_display_label.setObjectName("VideoLabel")

        self.display_video_path_line = QLineEdit()
        self.display_video_path_line.setClearButtonEnabled(True)
        self.display_video_path_line.setPlaceholderText("Select video or use webcam")

        self.start_button = QPushButton("Start Video")
        self.start_button.clicked.connect(self.startVideo)
        
        stop_button = QPushButton("Stop Video")
        stop_button.clicked.connect(self.stopCurrentVideo)

        # Create horizontal and vertical layouts
        side_panel_v_box = QVBoxLayout()
        side_panel_v_box.setAlignment(Qt.AlignTop)
        side_panel_v_box.addWidget(self.display_video_path_line)
        side_panel_v_box.addWidget(self.start_button)
        side_panel_v_box.addWidget(stop_button)

        side_panel_frame = QFrame()
        side_panel_frame.setMinimumWidth(200)
        side_panel_frame.setLayout(side_panel_v_box)

        main_h_box = QHBoxLayout()
        main_h_box.addWidget(self.video_display_label, 1)
        main_h_box.addWidget(side_panel_frame)

        # Create container widget and set main window's widget
        container = QWidget()
        container.setLayout(main_h_box)
        self.setCentralWidget(container)

    def setupMenu(self):
        """Simple menu bar to select local videos."""
        # Create actions for file menu
        open_act = QAction('Open...', self)
        open_act.setShortcut('Ctrl+O')
        open_act.triggered.connect(self.openVideoFile)

        # Create menu bar
        menu_bar = self.menuBar()
        menu_bar.setNativeMenuBar(False)

        # Create file menu and add actions
        file_menu = menu_bar.addMenu('File')
        file_menu.addAction(open_act)

    def startVideo(self):
        """Create and begin running the the worker thread to play the video."""
        self.thread_is_running = True
        self.start_button.setEnabled(False)
        self.start_button.repaint()

        # Create an instance of the worker thread if a user has chosen a local file
        if self.display_video_path_line.text() != "":
            video_file = self.display_video_path_line.text()
            self.video_thread_worker = VideoWorkerThread(self, video_file)
        else:
            # Use the webcam 
            self.video_thread_worker = VideoWorkerThread(self, 0)

        # Connect to the thread's signal to update the frames in the video_display_label 
        self.video_thread_worker.frame_data_updated.connect(self.updateVideoFrames)
        self.video_thread_worker.invalid_video_file.connect(self.invalidVideoFile)
        self.video_thread_worker.start() # Start the thread

    def stopCurrentVideo(self):
        """Stop the current video, process events, and clear the video_display_label."""
        if self.thread_is_running == True:
            self.thread_is_running = False  
            self.video_thread_worker.stopThread() 
            
            self.video_display_label.clear()
            self.start_button.setEnabled(True)

    def openVideoFile(self):
        """Open a video file and display the file's path in the line edit widget."""
        video_file, _ = QFileDialog.getOpenFileName(self, "Open Video", os.getenv('HOME'), "Videos (*.mp4 *.avi)")

        if video_file:
            self.display_video_path_line.setText(video_file) # Use selected file's path  
        else:
            QMessageBox.information(self, "Error", "No video was loaded.", QMessageBox.Ok)

    def updateVideoFrames(self, video_frame):
        """A video is a collection of images played together in quick succession. For each frame (image) in 
        the video, convert it to a QImage object to be displayed in the QLabel widget."""
        # Get the shape of the frame, height * width * channels. BGR/RGB/HSV images have 3 channels
        height, width, channels = video_frame.shape # Format: (rows, columns, channels)
        # Number of bytes required by the image pixels in a row; dependency on the number of channels
        bytes_per_line = width * channels
        # Create instance of QImage using data from the video file
        converted_Qt_image = QImage(video_frame, width, height, bytes_per_line, QImage.Format_RGB888)

        # Set the video_display_label's pixmap
        self.video_display_label.setPixmap(QPixmap.fromImage(converted_Qt_image).scaled(
                self.video_display_label.width(), self.video_display_label.height(), Qt.KeepAspectRatioByExpanding))

    def invalidVideoFile(self):
        """Display a dialog box to inform the user that an error occurred while loading the video."""
        QMessageBox.warning(self, "Error", "No video was loaded.", QMessageBox.Ok)
        self.start_button.setEnabled(True)

    def closeEvent(self, event):
        """Reimplement the closing event to ensure that the thread closes."""
        if self.thread_is_running == True:
            self.video_thread_worker.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = DisplayVideo()
    sys.exit(app.exec_())