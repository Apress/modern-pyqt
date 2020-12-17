"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, cv2
from numpy import ndarray, array
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QFrame, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QThread, pyqtSignal

style_sheet = """
    QLabel#VideoLabel{
        color: darkgrey;
        border: 2px solid darkgrey;
        qproperty-alignment: AlignCenter
    }"""

class VideoWorkerThread(QThread):
    """Worker thread for capturing video."""
    frame_data_updated = pyqtSignal(ndarray)

    def __init__(self, parent, video_file=None):
        super().__init__() 
        self.parent = parent
        self.video_file = video_file

    def run(self):
        """The code that we want to run in a separate thread, in this case
        capturing video using OpenCV, is placed in this function. run() is called
        after start()."""
        self.capture = cv2.VideoCapture(self.video_file) # 0 opens the default camera

        while self.parent.thread_is_running:
            # Read frames from the camera
            ret_val, frame = self.capture.read()
            
            if not ret_val:
                break # Error or reached the end of the video
            else:     
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Resize an image for faster detection
                frame = cv2.resize(frame, (600, 400))
                rects = self.createHOGDescriptor(frame)

                # Draw the detections (rects) in the frame; tr and br refer to the top-left and
                # bottom-left corners of the detected rects, respectively.
                for (x_tr, y_tr, x_br, y_br) in rects:
                    frame = cv2.rectangle(frame, (x_tr, y_tr), (x_br, y_br), (0, 0, 255), 2)
                self.frame_data_updated.emit(frame) 

    def createHOGDescriptor(self, frame):
        """Function creates the HOG Descriptor for human detection and returns the detections (rects)."""
        # Initialize OpenCV's HOG Descriptor and SVM classifier
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

        # Detect people in the image and return the bounding rectangles. Altering the parameters
        # in detectMultiScale() can affect the accuracy of detections. winStride refers to the 
        # number of steps the sliding window moves in the x and y directions; the sliding window 
        # is padded to improve accuracy; a smaller scale value will increase detection accuracy, 
        # but also increase processing time
        rects, weights = hog.detectMultiScale(frame, winStride=(4, 4), 
            padding=(8, 8), scale=1.1)
        # For each of the rects detected in an image, add the values for the corners
        # of the rect to an array 
        rects = array([[x, y, x + width, y + height] for (x, y, width, height) in rects])
        return rects

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
        self.setWindowTitle('5.2 - Human Detection GUI')
        
        self.thread_is_running = False

        self.setupWindow()
        self.show()

    def setupWindow(self):
        """Set up widgets in the main window."""
        self.video_display_label = QLabel()
        self.video_display_label.setObjectName("VideoLabel")

        self.start_button = QPushButton("Start Video")
        self.start_button.clicked.connect(self.startVideo)
        
        stop_button = QPushButton("Stop Video")
        stop_button.clicked.connect(self.stopCurrentVideo)

        # Create horizontal and vertical layouts
        side_panel_v_box = QVBoxLayout()
        side_panel_v_box.setAlignment(Qt.AlignTop)
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

    def startVideo(self):
        """Create and begin running the the worker thread to play the video."""
        self.thread_is_running = True
        self.start_button.setEnabled(False)
        self.start_button.repaint()

        # Create an instance of the worker thread using a local video file
        video_file = "media/people_mall.mp4"
        self.video_thread_worker = VideoWorkerThread(self, video_file)

        # Connect to the thread's signal to update the frames in the video_display_label 
        self.video_thread_worker.frame_data_updated.connect(self.updateVideoFrames)
        self.video_thread_worker.start() # Start the thread

    def stopCurrentVideo(self):
        """Stop the current video, process events, and clear the video_display_label."""
        if self.thread_is_running == True:
            self.thread_is_running = False  
            self.video_thread_worker.stopThread() 
            
            self.video_display_label.clear()
            self.start_button.setEnabled(True)

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

    def closeEvent(self, event):
        """Reimplement the closing event to ensure that the thread closes."""
        if self.thread_is_running == True:
            self.video_thread_worker.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = DisplayVideo()
    sys.exit(app.exec_())