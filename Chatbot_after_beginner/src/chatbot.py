
from src.command_handler import *
from src.trivia_game import *
from src.csvdata_handler import *
from src.weather_forcast import *
import logging
from datetime import datetime
import random
import sys
import pandas as pd


timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
logging.basicConfig(filename=f'log/chatbot-{timestamp}.log', encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger('chatbot') 

class Chatbot:
    
    """Chatbot class that handles the chatbot's logic and data.

    Attributes:
        args (list): List of command line arguments.
        df (pandas.DataFrame): Dataframe to store chatbot data.
        asked_questions (set): Set to store asked questions.
        data_file_path (str): Path to the data file.
        greetings (list): List of greeting messages.
        goodbyes (list): List of goodbye messages.

    Methods:
        greeting(): Displays a greeting message.
        get_greeting(): Returns a random greeting message.
        get_bye(): Returns a random goodbye message.
        possible_q(): Returns a list of possible questions.
        parse_question_input(arg_list): Parses the question input.
        add_row_to_csv(questions, subjects, answers, data_path): Adds a row to the CSV file.
        is_keyword_or_variation(input_text, subject_column, subject_variation_column): Checks if the input text is a keyword or variation.
        is_question_or_variation(input_text, question_column, variation_column): Checks if the input text is a question or variation.
        find_question_row_index(input_text, question_column, variation_column, df): Finds the row index of a question in the dataframe.
        remove_row_from_csv(df, questions, data_path): Removes a row from the CSV file.
        print_random_answer(input_text, questions_column, questions_var_column, answers_column, answers_var_column): Prints a random answer for the given question.
        print_related_questions(input_text, questions_column, subject_column, answers_column): Prints all related questions for the given subject.
        init_trivia(): Initializes the trivia mode.
        go_directly_to(): Goes directly to the the corresponding situation either user input or cli input mode.
        init_questions(): Initializes the chatbot and handles user input.
        read_data(): Reads the data from the CSV file.
        run_chatbot(): Runs the chatbot.

    """
    def __init__(self, data_file_path,args):
        self.args = args
        self.df = pd.DataFrame()
        self.asked_questions = set()
        self.data_file_path = data_file_path

    greetings = ["Hello! How can I help you?", "Hi there! What can I do for you?", "Greetings! How may I assist you today?"]
    goodbyes = ["Goodbye! Have a great day!", "Farewell! Come back soon!", "Goodbye, take care!"]
    
    def greeting(self):
        logging.info(print("Hello"))
        logging.info(print("How can I help you?"))
    
    def get_greeting(self):
        return random.choice(self.greetings)
    def get_bye(self):
        return random.choice(self.goodbyes)
    
    def possible_q(self):
        return possible_q(self.df)
    
    def parse_question_input(arg_list):
        return parse_question_input(arg_list
                                    )
    def add_row_to_csv(self, questions, subjects, answers, data_path):
        self.df = add_row_to_csv(self.df, questions, subjects, answers, data_path)

    def is_keyword_or_variation(self,input_text, subject_column, subject_variation_column):
        return is_keyword_or_variation(input_text, subject_column, subject_variation_column,self.df)
    
    def is_question_or_variation(self, input_text, question_column, variation_column):
        return is_question_or_variation(input_text, question_column, variation_column, self.df)

    def find_question_row_index(self, input_text, question_column, variation_column,df):
        return find_question_row_index(input_text, question_column, variation_column,df)
    
    def remove_row_from_csv(self,df,questions, data_path):
        return remove_row_from_csv(df,questions, data_path)
    
    def print_random_answer(self, input_text, questions_column, questions_var_column, answers_column, answers_var_column):
        return print_random_answer(input_text, questions_column, questions_var_column, answers_column, answers_var_column, self.df)

    def print_related_questions( self,input_text, questions_column, subject_column, answers_column):
        logging.info(print_related_questions( input_text, questions_column, subject_column, answers_column,self.df))
    
    def init_trivia(self):
        logging.info(init_trivia())

    def go_directly_to(self):
        logging.info(go_directly_to(self))



    def init_questions(self):
        """Initializes the chatbot and handles user input.

        This method prompts the user to ask a question and processes the input accordingly.
        If the user enters "bye", the chatbot will exit.
        If the user enters "trivia", the chatbot will initiate a trivia game.
        If the user enters a valid question, the chatbot will print a random answer.
        If the question is related to an event, the chatbot will also print the weather forecast for that event.
        If the user enters a keyword, the chatbot will print all related questions.
        If the user enters multiple inputs, each input will be processed individually.

        """
        logging.info('chtbot started reading questions') 
        while True:
            logging.info('Ask me something:') 
            user_input = input("Ask me something: ").lower().split(',')
            logging.info(f'input: {user_input}')
            
            # if user_input is one question
            
            if len(user_input) == 1:
                
                #if user_input is bye
                
                if user_input[0] == "bye":
                    logging.info('bye input detected, exitin') 
                    print(self.get_bye())
                    break
                
                #if user_input is trivia
                
                if user_input[0] == "trivia":
                    logging.info('trivia input detected, init trivia') 
                    self.init_trivia()
                    continue
                
                #if user_input is a question
                
                if self.is_question_or_variation(user_input[0], 'Question', 'Question_Variation'):
                    logging.info('question input question found, printing answer') 
                    answer_temp=self.print_random_answer(user_input[0], 'Question', 'Question_Variation', 'Answer', 'Answer_Variation') 
                    found, question_row_Index = find_question_row_index(user_input[0], 'Question', 'Question_Variation', self.df)
                    if found:
                        if keyword_of_question_is_event(question_row_Index,'Subject','Answer',self.df):
                            logging.info('question input is event, printing event')
                            print(answer_temp)
                            weather_forecast = get_weather_forecast(answer_temp)
                            print(weather_forecast)
                            continue
                    print(answer_temp)
                    self.asked_questions.add(user_input[0])
                    continue
                
                #if user_input is a keyword
                
                if self.is_keyword_or_variation(user_input[0], 'Subject', 'Subject_Variation'):
                    logging.info('subject input keyword found, printing all related questions') 
                    self.print_related_questions(user_input[0], 'Question', 'Subject', 'Answer')
                    continue
                
                #if user_input is not a question or keyword
                
                else:
                    logging.info('no valid input found, printing possible questions')
                    print("I'm not sure how to answer that question ")
                    print("do you me to print all possible questions?")
                    if input("y/n: ") == "y":
                        possible_q(self.df)
                    else:
                        continue
            
            #if user_input is multiple questions each will be processed individually
            
            else:
                logging.info('multiple inputs detected')
                logging.info(user_input)
                for question in user_input:
                    question = question.strip()
                    
                    #if user_input is bye
                    
                    if question == "bye":
                        logging.info('bye input detected, exitin')
                        print(self.get_bye())
                        break

                    #if user_input is trivia
                    
                    if self.is_question_or_variation(question, 'Question', 'Question_Variation'):
                        logging.info('question input question found, printing answer')
                        answer_temp=self.print_random_answer(question, 'Question', 'Question_Variation', 'Answer', 'Answer_Variation') 
                        found, question_row_Index = find_question_row_index(question, 'Question', 'Question_Variation', self.df)
                        if found:
                            if keyword_of_question_is_event(question_row_Index,'Subject','Answer',self.df):
                                logging.info('question input is event, printing event')
                                print(answer_temp)
                                weather_forecast = get_weather_forecast(answer_temp)
                                print(weather_forecast)
                                continue
                        print(answer_temp)
                        self.asked_questions.add(question)
                        continue
                    
                    #if user_input is a keyword
                    
                    if self.is_keyword_or_variation(question, 'Subject', 'Subject_Variation'):
                        logging.info('subject input keyword found, printing all related questions')
                        self.print_related_questions(question, 'Question', 'Subject', 'Answer')
                        continue
                    
                    #if user_input is not a question or keyword
                    
                    else:
                        logging.info('no valid input found, printing possible questions')
                        print("I'm not sure how to answer that question ")
                        print("do you me to print all possible questions?")
                        if input("y/n: ") == "y":
                            possible_q(self.df)
                        else:
                            continue

    # function to read the csv file 
    
    def read_data(self):
        try:
            file_path = self.data_file_path
            self.df = pd.read_csv(file_path, encoding='latin1')
        except FileNotFoundError:
            logging.error("Error: Invalid file path. File not found.")
        except PermissionError:
            logging.error("Error: Insufficient access privilege rights. Permission denied.")
        except pd.errors.EmptyDataError:
            logging.error("Error: Empty CSV file.")
        except pd.errors.ParserError:
            logging.error("Error: Corrupted CSV file or unsupported format within CSV file.")
        except Exception as e:
            logging.error(f"Error reading CSV: {e}")



    def run_chatbot(self):
        self.read_data()
        self.go_directly_to()



if __name__ == "__main__":
    data_path='data/chatbotdata.csv'    
    chatbot = Chatbot(data_path, sys.argv)
    chatbot.run_chatbot()
