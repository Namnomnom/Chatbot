import os
import sys
from bin.main import *
from src.question_handler import *
from src.cli_handler import *
from src.csvdata_handler import *
from src.chatbot import *
import logging
from datetime import datetime

logger = logging.getLogger('chatbot') 
import unittest


log_dir = 'CHATBOT/log'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)



def parse_question_input(arg_list):
    """
    Parses a list of input arguments and extracts questions, subjects, and answers.

    Args:
        arg_list (list): A list of input arguments in the format 'question:subject:answer'.

    Returns:
        tuple: A tuple containing three lists: questions, subjects, and answers.
    """
    #splitting the input arguments received from the command line to question, subject and answer
    #this function is called when --addQuestion is passed as argument

    questions = []
    subjects = []
    answers = []
    for entry in arg_list:
        parts = entry.split(':')
        if len(parts) == 3:
            question, subject, answer = parts
            questions.append(question)
            subjects.append(subject)
            answers.append(answer)
        else:
            print(f"Invalid input format: {entry}. Expected format: 'question:subject:answer'")
            continue
    return questions, subjects, answers



def go_directly_to(chatbot):
    """
    This function handles the command line arguments and performs the corresponding actions.
    
    Args:
        chatbot: The chatbot object.
    """
    #if question is passed as argument
    
    if chatbot.args.question:
        logger.info("Question in cli asked") 
        user_question = chatbot.args.question.lower()
        if chatbot.is_question_or_variation(user_question, 'Question', 'Question_Variation'):
            logger.info("Question found in data")
            logger.info( chatbot.print_random_answer(user_question, 'Question', 'Question_Variation', 'Answer', 'Answer_Variation'))
            print(chatbot.print_random_answer(user_question, 'Question', 'Question_Variation', 'Answer', 'Answer_Variation'))
            logger.info("answer random printed")
            chatbot.asked_questions.add(user_question)
    
    #if add is passed as argument
    
    if chatbot.args.add:
        if chatbot.args.Q and chatbot.args.answer and chatbot.args.subject:
            logger.info("add question in cli asked")
            parsed_subjects = chatbot.args.subject
            parsed_answers = chatbot.args.answer
            parsed_question = chatbot.args.Q

            if not chatbot.is_question_or_variation(parsed_question, 'Question', 'Question_Variation'):
                logger.info("Question not in data")
                add_row_to_csv(chatbot.df,parsed_question, parsed_subjects, parsed_answers,'c:\\Users\\smoti\\Documents\\digi\\digitec_chatbot\\data\\chatbotdata.csv')
                logger.info("Question added to data")
            else:
                print("Err Question already in data")
                logger.info("Question already in data")
        else:
            print("Invalid input format for --add: required format: --add --Q \"QuestionA?\" --answer \"AnswerA\" --subject \"Subject\"")
            logger.info("Invalid input format for --add: required format: --add --Q \"QuestionA?\" --answer \"AnswerA\" --subject \"Subject\"")
    
    #if allQs is passed as argument
    
    if chatbot.args.allQs:
        logger.info("all questions in cli asked")
        chatbot.possible_q()
        logger.info("all questions printed")

    #if importcsv is passed as argument
    
    if chatbot.args.importcsv:
        logger.info("import csv in cli asked")
        import_csv(chatbot.df,chatbot.args.importcsv,'data/chatbotdata.csv')
        logger.info("csv import function called")
        
    #if addQuestion is passed as argument 
    
    if chatbot.args.addQuestion:
        logger.info("add question in cli asked")
        parsed_questions, parsed_subjects, parsed_answers = parse_question_input(chatbot.args.addQuestion)
        if not chatbot.is_question_or_variation(parsed_questions, 'Question', 'Question_Variation'):
            if parsed_questions is not None:
                print("Parsed Questions:", parsed_questions)
                print("Parsed Subjects:", parsed_subjects)
                print("Parsed Answers:", parsed_answers)
                add_row_to_csv(chatbot.df,parsed_questions, parsed_subjects, parsed_answers,'c:\\Users\\smoti\\Documents\\digi\\digitec_chatbot\\data\\chatbotdata.csv')
        else:
            print('Question is already added')
            
    #if removeQuestion is passed as argument
    
    if chatbot.args.removeQuestion:
        user_question = chatbot.args.removeQuestion[0]
        chatbot.remove_row_from_csv(chatbot.df,user_question,'data/chatbotdata.csv')
    
    #if chatbot.args.log_mode: 
    #    logging.basicConfig(filename=os.path.join(log_dir, 'app.log'), level=chatbot.args.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    #    logging.basicConfig(filename='C:/Users/smoti/Documents/digi/digitec_chatbot/logs/app.log', level=chatbot.args.log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    #    logging.warning('Some potential issue occurred while looking up answers.')
    
    #if help is passed as argument
    
    if chatbot.args.helpme:
        print("Help")
        logger.info("Help")
        print("Here are possible command line arguments: \n --debug: run in debug mode \n--question: ask a question directly from the command line \n --add: add a question directly from the command line \n--allQs: print all questions \n--importcsv: import csv file \n--addQuestion: add question with subject and answer \n--removeQuestion: remove question with subject and answer \n--log_mode: log mode \n--log_level: log level \n--help: help")
        logger.info("Here are possible command line arguments:")
    
    #if debug is passed as argument
    
    if chatbot.args.debug:
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'tests')))
        tests = unittest.defaultTestLoader.discover('tests')
        unittest.TextTestRunner().run(tests)
    
    else:
        logger.info("Program started")
        chatbot.greeting()
        chatbot.init_questions()