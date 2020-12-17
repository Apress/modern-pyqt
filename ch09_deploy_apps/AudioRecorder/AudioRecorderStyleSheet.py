"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Style sheet for the Audio Recorder GUI

style_sheet = """
    QWidget {
        background-color: #FFFFFF
    }

    QPushButton {
        background-color: #AFAFB0;
        border: 2px solid #949495;
        border-radius: 4px;
        padding: 5px
    }

    QPushButton:hover {
        background-color: #C2C2C4;
    }

    QPushButton:pressed {
        background-color: #909091;
    }

    /* Set up the appearance of the start button for normal, hovered
    and pressed states. */
    QPushButton#StartButton {
        background-color: #FFFFFF; 
        image: url(:/resources/images/mic.png);
        border: none
    }

    QPushButton#StartButton:hover {
        image: url(:/resources/images/mic_hover.png);
    }

    QPushButton#StartButton:pressed {
        image: url(:/resources/images/mic_pressed.png);
    }

    QPushButton#StartButton:disabled {
        image: url(:/resources/images/mic_disabled.png);
    }

    /* Set up the appearance of the stop button for normal, hovered
    and pressed states. */
    QPushButton#StopButton {
        background-color: #FFFFFF;
        image: url(:/resources/images/stop.png);
        border: none
    }

    QPushButton#StopButton:hover {
        image: url(:/resources/images/stop_hover.png);
    }

    QPushButton#StopButton:pressed {
        image: url(:/resources/images/stop_pressed.png);
    }
"""