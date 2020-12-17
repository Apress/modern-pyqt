"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys, smtplib
from email.message import EmailMessage
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QDialog, QMessageBox, QDialogButtonBox,
    QStatusBar, QGridLayout, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class PasswordDialog(QDialog):

    def __init__(self, parent):
        super().__init__()
        # [INFO] This line only checks if sender and recipient line edits are not 
        # blank. There are other checks you could make, such as if the @ symbol 
        # exists, or if the email extension is valid.
        if parent.sender_address.text() != "" and parent.recipient_address.text() != "":
            self.setWindowTitle("Submit Gmail Password")
            self.setFixedSize(300, 100)
            self.setModal(True)

            enter_password_label = QLabel("Enter Password:")
            self.enter_password_line = QLineEdit()
            self.enter_password_line.setEchoMode(QLineEdit.Password)

            # Create nested layout for widgets to enter the password
            # and for the QDialogButtonBox
            password_h_box = QHBoxLayout()
            password_h_box.addWidget(enter_password_label)
            password_h_box.addWidget(self.enter_password_line)
            
            buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            button_box = QDialogButtonBox(buttons)
            button_box.accepted.connect(self.accept)
            button_box.rejected.connect(self.reject)

            dialog_v_box = QVBoxLayout()
            dialog_v_box.addLayout(password_h_box)
            dialog_v_box.addWidget(button_box)
            self.setLayout(dialog_v_box)
        else:
            QMessageBox.information(self, "Missing Information",
                "Sender or Recipient Information is Empty.", QMessageBox.Ok)

class EmailGUI(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and display its contents."""
        self.setMinimumSize(800, 500)
        self.setWindowTitle('7.2 - Email GUI')

        self.setupWindow()
        self.show()

    def setupWindow(self):
        """Set up the widgets for inputting the headers and body 
        of the email."""
        window_label = QLabel("Send a Simple Email")
        window_label.setFont(QFont("Courier", 24))
        window_label.setAlignment(Qt.AlignCenter)

        sender_label = QLabel("From:")
        self.sender_address = QLineEdit()
        self.sender_address.setPlaceholderText("your_email@gmail.com")

        recipient_label = QLabel("To:")
        self.recipient_address = QLineEdit()
        self.recipient_address.setPlaceholderText("friend@email.com")

        subject_label = QLabel("Subject:")
        self.subject_line = QLineEdit()

        # Layout for the sender, recipient and subject widgets
        header_grid = QGridLayout()
        header_grid.addWidget(sender_label, 0, 0)
        header_grid.addWidget(self.sender_address, 0, 1)
        header_grid.addWidget(recipient_label, 1, 0)
        header_grid.addWidget(self.recipient_address, 1, 1)
        header_grid.addWidget(subject_label, 2, 0)
        header_grid.addWidget(self.subject_line, 2, 1)

        self.email_body = QTextEdit() # Input widget for creating email contents

        send_button = QPushButton("Send")
        send_button.clicked.connect(self.inputPassword)

        bottom_h_box = QHBoxLayout()
        bottom_h_box.addWidget(QWidget(), 1)
        bottom_h_box.addWidget(send_button)

        # Nested layout for all widgets and layouts
        main_v_box = QVBoxLayout()
        main_v_box.addWidget(window_label)
        main_v_box.addSpacing(10)
        main_v_box.addLayout(header_grid)
        main_v_box.addWidget(self.email_body)
        main_v_box.addLayout(bottom_h_box)

        container = QWidget()
        container.setLayout(main_v_box)
        self.setCentralWidget(container)

        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar) # Create status bar

    def inputPassword(self):
        """Create an instance of the PasswordDialog class and input the Gmail
        account password."""
        self.password_dialog = PasswordDialog(self)
        if self.password_dialog.exec_() and self.password_dialog.enter_password_line.text() != "":
            self.password_dialog.close()
            self.sendEmail()
        else:
            pass

    def sendEmail(self):
        """Compose the email headers and contents. Use smtplib to login to your Gmail account
        and send an email. Success or errors will be displayed in the status bar accordingly.""" 
        # Define the headers and content of the email
        message = EmailMessage()
        message['Subject'] = self.subject_line.text()
        message['From'] = self.sender_address.text()
        message['To'] = self.recipient_address.text()

        # Convert the text in the QTextEdit to HTML
        message.add_alternative(self.email_body.toHtml(), subtype="html")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            try:
                # Login to your Gmail username and password
                smtp.login(self.sender_address.text(), self.password_dialog.enter_password_line.text())
                smtp.send_message(message)

                # Display feedback in the status bar and clear input widgets
                self.status_bar.showMessage("Your email was sent!", 5000) 
                self.subject_line.clear()
                self.recipient_address.clear()
                self.email_body.clear()
            except smtplib.SMTPResponseException as error:
                error_message = "Email failed: {}, {}".format(error.smtp_code, error.smtp_error)
                self.status_bar.showMessage(error_message, 20000) # Display error for 20 seconds

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmailGUI()
    sys.exit(app.exec_())