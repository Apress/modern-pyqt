"""
Written by Joshua Willman
Featured in "Modern Pyqt - Create GUI Applications for Project Management, Computer Vision, and Data Analysis"
"""
# Import necessary modules 
from chatterbot import ChatBot # Import the chatbot
from chatterbot.trainers import ListTrainer # Method to train chatterbot

chatbot = ChatBot('Chatty') # Create the ChatBot called Chatty

# Create the dialog
conversation = [
    "Hello",
    "Hi! How are you?",
    "I'm happy. How about you?",
    "Hungry.",
    "Let's have lunch!",
    "Let's go!"]

trainer = ListTrainer(chatbot) # Create trainer
trainer.train(conversation) # Train the chatbot

while True:
    try:
        user_input = input('You: ')
        bot_response = chatbot.get_response(user_input)
        print('Bot: ' +  str(bot_response))
    except(KeyboardInterrupt, EOFError, SystemExit):
        break