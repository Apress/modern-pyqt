"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QMessageBox, QMenu, 
    QFileDialog, QVBoxLayout, QSystemTrayIcon)
from PyQt5.QtMultimedia import QAudioRecorder, QAudioEncoderSettings, QMultimedia
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QFont
from AudioRecorderStyleSheet import style_sheet
import resources

class AudioRecorder(QWidget):    

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents to the screen."""
        self.setFixedSize(360, 540)
        self.setWindowTitle('9.1 - Audio Recorder')

        self.audio_path = "" # Empty variable for path to audio file
                
        self.setupWindow()
        self.setupSystemTrayIcon()
        self.show()

    def setupWindow(self):
        """Set up widgets in the main window and the QAudioRecorder instance."""
        # Set up two push buttons (the app's first "screen")
        self.select_path_button = QPushButton("Select Audio Path")
        self.select_path_button.setObjectName("SelectFile")
        self.select_path_button.setFixedWidth(140)
        self.select_path_button.clicked.connect(self.selectAudioPath)

        self.start_button = QPushButton()
        self.start_button.setObjectName("StartButton")
        self.start_button.setEnabled(False)
        self.start_button.setFixedSize(105, 105)
        self.start_button.clicked.connect(self.startRecording)

        # Set up the labels and stop button (the app's second "screen")
        self.recording_label = QLabel("Recording...")
        self.recording_label.setFont(QFont("Helvetica [Cronyx]", 32))
        self.recording_label.setVisible(False)
        self.recording_label.setAlignment(Qt.AlignHCenter)
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont("Helvetica [Cronyx]", 18))
        self.time_label.setObjectName("Time")
        self.time_label.setVisible(False)
        self.time_label.setAlignment(Qt.AlignHCenter)

        self.stop_button = QPushButton()
        self.stop_button.setObjectName("StopButton")
        self.stop_button.setFixedSize(65, 65)
        self.stop_button.setVisible(False)
        self.stop_button.clicked.connect(self.stopRecording)

        # Set up the main layout
        self.main_v_box = QVBoxLayout()
        self.main_v_box.setAlignment(Qt.AlignHCenter)
        self.main_v_box.addWidget(self.select_path_button)
        # Force select_path_button to be centered in the window
        self.main_v_box.setAlignment(self.select_path_button, Qt.AlignCenter)
        self.main_v_box.addStretch(3)
        self.main_v_box.addWidget(self.start_button)
        self.main_v_box.setAlignment(self.start_button, Qt.AlignCenter)
        self.main_v_box.addWidget(self.recording_label)
        self.main_v_box.addWidget(self.time_label)
        self.main_v_box.addStretch(3)
        self.main_v_box.addWidget(self.stop_button)
        self.main_v_box.setAlignment(self.stop_button, Qt.AlignCenter)
        self.main_v_box.addStretch(1)
        
        self.setLayout(self.main_v_box) # Set the beginning layout

        # Specify audio encoder settings
        audio_settings = QAudioEncoderSettings()
        # Depending upon your platform or the codecs that you have available, you 
        # will need to change the codec. For Linux users if you are having issues 
        # use "audio/x-vorbis", and then select the .ogg extension when saving 
        # the file
        audio_settings.setCodec("audio/wav")
        audio_settings.setQuality(QMultimedia.HighQuality)

        # Create instance of QAudioRecorder for recording audio
        self.audio_recorder = QAudioRecorder()
        # Uncomment to discover possible codecs supported on your platform
        #print(self.audio_recorder.supportedAudioCodecs())
        self.audio_recorder.setEncodingSettings(audio_settings)
        self.audio_recorder.durationChanged.connect(self.displayTime)  

    def setupSystemTrayIcon(self):
        """Set up system tray icon and context menu. User can re-open the window if
        it was closed or quit the application using the tray menu."""
        self.tray_icon = QSystemTrayIcon(QIcon(":/resources/images/mic_icon.png"))

        # Create the actions and context menu for the tray icon
        tray_menu = QMenu()

        open_act = tray_menu.addAction("Open")
        open_act.triggered.connect(self.show)
        tray_menu.addSeparator()
        quit_act = tray_menu.addAction("Quit")
        quit_act.triggered.connect(QApplication.quit)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def selectAudioPath(self):
        """Open file dialog and choose the directory for saving the audio file."""
        path, _ = QFileDialog.getSaveFileName(self, "Save Audio File",
            os.getenv("HOME"), "WAV (*.wav)")

        if path:
            self.audio_path = path
            self.start_button.setEnabled(True)
        else:
            QMessageBox.information(self, "Error",
                "No directory selected.", QMessageBox.Ok)

    def startRecording(self):
        """Set up the audio output file location, reset widget states.
        Also starts the timer and begins recording. """
        self.audio_recorder.setOutputLocation(QUrl.fromLocalFile(self.audio_path))   

        # Set widget states
        self.select_path_button.setVisible(False)
        self.start_button.setVisible(False)
        self.recording_label.setVisible(True)
        self.time_label.setVisible(True)
        self.time_label.setText("00:00") # Update the label
        self.stop_button.setVisible(True)

        # Start the timer and begin recording
        self.audio_recorder.record()

    def stopRecording(self):
        """Stop recording, stop the timer, and reset widget states."""
        self.audio_recorder.stop()

        # Reset widget states
        self.select_path_button.setVisible(True)
        self.start_button.setVisible(True)
        self.recording_label.setVisible(False)
        self.time_label.setVisible(False)
        self.stop_button.setVisible(False)

    def displayTime(self, duration):
        """Calculate the time displayed in the time_label widget."""
        minutes, seconds = self.convertTotalTime(duration)
        time_recorded = "{:02d}:{:02d}".format(minutes, seconds)
        self.time_label.setText(time_recorded)

    def convertTotalTime(self, time_in_milli):
        """Convert time from milliseconds."""
        minutes = (time_in_milli / (1000 * 60)) % 60
        seconds = (time_in_milli / 1000) % 60
        return int(minutes), int(seconds)  

    def closeEvent(self, event):
        """Display a message in the system tray when the main window has been closed."""
        self.tray_icon.showMessage("Notification", "Audio Recorder is still running.", 8000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(":/resources/images/mic_icon.png"))
    app.setQuitOnLastWindowClosed(False) # Closing the window does not close the application
    app.setStyleSheet(style_sheet)
    window = AudioRecorder()
    sys.exit(app.exec_())