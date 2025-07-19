from src.question_handler import *
from src.chatbot import *
from src.command_handler import *
from src.csvdata_handler import *

import argparse

def parse_arguments():
    
    parser = argparse.ArgumentParser(description="Chatbot CLI")
    parser.add_argument('--debug', action='store_true', help='Enable debugging mode')
    parser.add_argument('--log-mode', action='store_true', help='Enable logging mode') 
    parser.add_argument('--log-level', choices=['INFO', 'WARNING'], default='WARNING', help='Set logging level (default: WARNING)')
    parser.add_argument('--helpme', action='store_true', help='Help')
    parser.add_argument('--data-file', type=str, default='data/chatbotdata.csv', help='Path to the data file')
    parser.add_argument('--question', type=str, help='go to Questions')
    parser.add_argument('--importcsv', type=str, help='import using csv path in this form "path" ')
    parser.add_argument('--allQs', action='store_true', help='list all possible Questions')
    parser.add_argument('--removeQuestion', type=str, nargs='+', help='remove a question in the format "question"')
    parser.add_argument('--addQuestion', type=str, nargs='+', help='add questions in the format "question:subject:answer"')
    parser.add_argument('--add', action='store_true', help='add questions --add --Q \"QuestionA?\" --answer \"AnswerA\" --subject \"Subject\"')
    parser.add_argument('--answer', type=str, help='answer for the question')
    parser.add_argument('--subject', type=str, help='subject for the question')
    parser.add_argument('--Q', type=str, help='the question to be added')
    args = parser.parse_args()

    return args
