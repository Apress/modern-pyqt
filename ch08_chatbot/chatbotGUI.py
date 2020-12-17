"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules
import sys
from chatterbot import ChatBot, utils
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QListView, 
    QMessageBox, QVBoxLayout, QStyledItemDelegate)
from PyQt5.QtCore import (Qt, QAbstractListModel, QMargins, QSize, QRect, QPoint, 
    QThread, pyqtSignal)
from PyQt5.QtGui import QIcon, QColor, QImage, QPolygon

style_sheet = """ 
    QPushButton {
        background: #83E56C /* Green */
    }

    QListView {
        background: #FDF3DD
    }"""

class ChatWorkerThread(QThread):
    # Signal emitted when the chatbot is finished training
    training_finished = pyqtSignal()

    def __init__(self, chatbot):
        super().__init__()
        self.chatbot = chatbot

    def run(self):
        """This function handles training the chatbot. Once the training is complete, the 
        training_finished signal is emitted, which allows the user to begin chatting."""
        self.trainer = ChatterBotCorpusTrainer(self.chatbot)
        self.trainer.train("chatterbot.corpus.english")
        self.training_finished.emit()
        
class ChatLogModel(QAbstractListModel):

    def __init__(self):
        super().__init__()
        self.chat_messages = []

    def rowCount(self, index):
        """Necessary to include rowCount() when subclassing QAbstractListModel. 
        For this program, we only need to update the the number of rows in the model,
        which is based on the length of chat_messages."""
        return len(self.chat_messages)

    def data(self, index, role=Qt.DisplayRole):
        """Necessary to include data() when subclassing QAbstractListModel. Retrieves 
        items from the list and returns data specified by the role, which in this case 
        is displayed as text."""
        if role == Qt.DisplayRole:
            return self.chat_messages[index.row()]

    def appendMessage(self, user_input, user_or_chatbot):
        """First, append new messages to chat_messages. Doing so will update the number
        of rows and indexes in the model (rowCount()), which will then update the data()."""
        self.chat_messages.append([user_input, user_or_chatbot])
        # Emit signal to indicate that the layout of items in the model has changed
        self.layoutChanged.emit() 

class DrawSpeechBubbleDelegate(QStyledItemDelegate):

    def __init__(self):
        super().__init__()
        self.image_offset = 5 # Horizontal offset for the image 
        # The following variables are used when drawing the speech bubbles
        self.side_offset, self.top_offset = 40, 5 
        self.tail_offset_x, self.tail_offset_y = 30, 0
        self.text_side_offset, self.text_top_offset = 50, 15

    def paint(self, painter, option, index):
        """Reimplement the delegate's paint() function. Renders the delegate using the specified QPainter 
        (painter) and QStyleOptionViewItem (option) for the item being drawn at given index (the row value).
        This function paints the item."""
        text, user_or_chatbot = index.model().data(index, Qt.DisplayRole)
        image, image_rect = QImage(), QRect() # Initialize objects for the user and chahbot icons
        color, bubble_margins = QColor(), QMargins() # Initialize objects for drawing speech bubbles
        tail_points = QPolygon() # Initialize QPolygon object for drawing the tail on the speech bubbles

        # Use user_or_chatbot value to select the image to display, the color of the pen and the
        # brush. Set the margins for speech bubble. Set the points for the speech bubble's tail.
        if user_or_chatbot == "chatbot":
            image.load("images/bot.png")
            image_rect = QRect(QPoint(option.rect.left() + self.image_offset, option.rect.center().y() - 12), QSize(24, 24))
            color = QColor("#83E56C")
            bubble_margins = QMargins(self.side_offset, self.top_offset, self.side_offset, self.top_offset)
            tail_points = QPolygon([QPoint(option.rect.x() + self.tail_offset_x, option.rect.center().y()),
                           QPoint(option.rect.x() + self.side_offset, option.rect.center().y() - 5),
                           QPoint(option.rect.x() + self.side_offset, option.rect.center().y() + 5)])
        elif user_or_chatbot == "user":
            image.load("images/user.png")
            image_rect = QRect(QPoint(option.rect.right() - self.image_offset - 24, option.rect.center().y() - 12), QSize(24, 24))
            color = QColor("#38E0F9")
            bubble_margins = QMargins(self.side_offset, self.top_offset, self.side_offset, self.top_offset)
            tail_points = QPolygon([QPoint(option.rect.right() - self.tail_offset_x, option.rect.center().y()),
                           QPoint(option.rect.right() - self.side_offset, option.rect.center().y() - 5),
                           QPoint(option.rect.right() - self.side_offset, option.rect.center().y() + 5)])

        # Draw the image next to the speech bubble
        painter.drawImage(image_rect, image)

        # Set the QPainter's pen and brush colors; draw the speech bubble and tail
        painter.setPen(color)
        painter.setBrush(color)
        # Remove the margins from the rectangle to shrink its size 
        painter.drawRoundedRect(option.rect.marginsRemoved(bubble_margins), 5, 5)
        painter.drawPolygon(tail_points)

        # Draw the text in the speech bubble
        painter.setPen(QColor("#4A4C4B")) # Reset pen color for the text
        text_margins = QMargins(self.text_side_offset, self.text_top_offset, self.text_side_offset, self.text_top_offset)
        painter.drawText(option.rect.marginsRemoved(text_margins), Qt.AlignVCenter | Qt.TextWordWrap, text)

    def sizeHint(self, option, index):
        """Reimplement to figure out the size of the item displayed at the given index.
        Uses option to figure out the style information, in this case, the margins of the speech bubble."""
        text, user_or_chatbot = index.model().data(index, Qt.DisplayRole)
        font_size = QApplication.fontMetrics() # Calculate the size of the text 
        text_margins = QMargins(self.text_side_offset, self.text_top_offset, self.text_side_offset, self.text_top_offset)

        # Remove the margins, get the rectangle for the font, and add the margins back in
        rect = option.rect.marginsRemoved(text_margins) 
        rect = font_size.boundingRect(rect, Qt.TextWordWrap, text)
        rect = rect.marginsAdded(text_margins)
        return rect.size()
    
class Chatbot(QWidget):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """Initialize the window and its contents."""
        self.setMinimumSize(450, 600)
        self.setWindowTitle("8.1 - PyQt Chatbot")
        self.setWindowFlag(Qt.Window)

        self.chat_started = False

        self.setupWindow()
        self.show()

    def setupWindow(self):
        """Set up the widgets and model/view instances for the main window."""
        self.chat_button = QPushButton(QIcon("images/chat.png"), "Start Chat")
        self.chat_button.setLayoutDirection(Qt.RightToLeft)
        self.chat_button.pressed.connect(self.chatButtonPressed)

        # Create the model for keeping track of new messages (data), the list view 
        # for displaying the chat log, and the delegate for drawing the items in the list view
        self.model = ChatLogModel()
        self.chat_log_view = QListView()
        self.chat_log_view.setModel(self.model)

        message_delegate = DrawSpeechBubbleDelegate()
        self.chat_log_view.setItemDelegate(message_delegate)

        # Create the QLineEdit widget for entering text
        self.user_input_line = QLineEdit()
        self.user_input_line.setMinimumHeight(24)
        self.user_input_line.setPlaceholderText("Press 'Start Chat' to begin chatting...")
        self.user_input_line.returnPressed.connect(self.enterUserMessage)
        
        main_v_box = QVBoxLayout()
        main_v_box.setContentsMargins(0, 2, 0, 10)
        main_v_box.addWidget(self.chat_button, Qt.AlignRight)
        main_v_box.setSpacing(10)
        main_v_box.addWidget(self.chat_log_view)
        main_v_box.addWidget(self.user_input_line)
        self.setLayout(main_v_box)

    def chatButtonPressed(self):
        """When the user begins chatting, the appearance and state of the chat_button are set, 
        and the chatbot is created. The user can also end the chat."""
        button = self.sender()
        if button.text() == "Start Chat":
            self.chat_button.setText("End Chat")
            self.chat_button.setIcon(QIcon("images/end.png"))
            self.chat_button.setStyleSheet("background: #EC7161") # Red
            self.chat_button.setDisabled(True)
            self.createChatbot() 
        elif button.text() == "End Chat":
            self.endCurrentChat()

    def enterUserMessage(self):
        """Get the text from the line edit widget and append the message to the model. Then
        display the chatbot's response."""
        user_input = self.user_input_line.text()
        if user_input != "" and self.chat_started == True:
            self.model.appendMessage(user_input, "user")
            self.displayChatbotResponse(user_input)
            self.user_input_line.clear() # Clear the QLineEdit's text
    
    def displayChatbotResponse(self, user_input):
        """Get the response from the chatbot, convert the reply to a string and 
        append the text to the model where it will be added to the window."""
        chatbot_reply = self.chatbot.get_response(user_input)
        self.model.appendMessage(str(chatbot_reply), "chatbot")
        # Uncomment to get the time it takes for the chatbot to respond
        #print(utils.get_response_time(self.chatbot))

    def createChatbot(self):
        """Create the chatbot and train it in a separate thread."""    
        self.chatbot = ChatBot("Chatbot", storage_adapter="chatterbot.storage.SQLStorageAdapter", 
            database_uri='sqlite:///database.sqlite3',
            logic_adapters=[{"import_path": "chatterbot.logic.BestMatch",
                "statement_comparison_function": LevenshteinDistance}])

        self.chat_worker = ChatWorkerThread(self.chatbot) # Create worker thread
        self.chat_worker.training_finished.connect(self.trainingFinished)

        # Feedback for the user. Begin the thread for trainig the chatbot
        self.model.appendMessage("[INFO] Chatbot is learning. Please wait a moment.", "chatbot")
        self.chat_worker.start()

    def trainingFinished(self):
        """Once the chatbot has been trained, display messages to the user and start chatting."""
        self.model.appendMessage("[INFO] Chatbot is ready to begin chatting with you.", "chatbot")
        self.model.appendMessage("Welcome to Chatbot. This chatbot gets smarter the more you talk with it. Type anything to get started.", "chatbot")
        self.user_input_line.setPlaceholderText("Type your message and press 'Enter'")
        self.chat_started = True
        self.chat_button.setDisabled(False) # Enable the chat_button

    def endCurrentChat(self):
        """Display a QMessageBox to the user asking if they want to quit the current chat."""
        choice = QMessageBox.question(self, "End Chat", 
            "The chat history will be deleted. Are you sure you want to end the chat?", 
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if choice == QMessageBox.Yes:
            # Clearing the list will set the number of rows to 0 and clear the chat area
            self.model.chat_messages = [] 
            self.user_input_line.setPlaceholderText("Press 'Start Chat' to begin chatting...")
            self.chat_button.setText("Start Chat")
            self.chat_button.setIcon(QIcon("images/chat.png"))
            self.chat_button.setStyleSheet("background: #83E56C") # Green
            self.chat_started = False 
        else:
            self.model.appendMessage("I thought you were going to leave me.", "chatbot")

    def closeEvent(self, event):
        """Display a dialog box to confirm that the user wants to close the application while in a chat."""
        if self.chat_started:
            choice = QMessageBox.question(self, 'Leave Chat?', "Are you sure you want to leave the chat?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if choice == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    window = Chatbot()
    sys.exit(app.exec_())