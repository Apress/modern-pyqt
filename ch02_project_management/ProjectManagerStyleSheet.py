"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Style sheet for the Project Manager GUI
style_sheet = """
    QWidget{ /* Main window's background color */
        background-color: #ACADAD
    }

    QFrame#ContainerFrame{ /* Style border for TaskContainer class */
        background-color: #8B8E96;
        border-bottom-left-radius: 4px;
	    border-bottom-right-radius: 4px
    }

    QFrame:hover#Task{ /* Indicate that the object is interactive and 
        can be dragged when the user hovers over it */
        border: 3px solid #2B2B2B
    }

    QLabel#TaskHeader{ /* Style header for dialog box */
        background-color: #8B8E96;
        qproperty-alignment: AlignLeft;
        padding: 0px 0px;
    }
    
    QLabel#TaskLabel{ /* Set alignment for QLabel in TaskWidget class */
        qproperty-alignment: AlignLeft;
    }

    QLabel#DescriptionLabel{ /* Style for label in dialog box */
        background-color: #8B8E96;
        qproperty-alignment: AlignLeft;
        padding: 0px 0px;
        font: 13px 
    }

    QLabel{ /* Style for QLabel objects for TaskContainer's title */
        color: #EFEFEF;
        qproperty-alignment: AlignCenter;
        border-top-left-radius: 4px; border-top-right-radius: 4px;
        padding: 10px 0px;
        font: bold 15px 
    }

    QPushButton{ 
        color: #4E4C4C;
        font: 14px 'Helvetica'
    }

    QPushButton#Task{
        color: #EFEFEF
    }

    QDialog{
        background-color: #8B8E96
    }
    
    QLineEdit{
        background-color: #FFFFFF
    }
    
    QTextEdit{
        background-color: #FFFFFF
    }"""