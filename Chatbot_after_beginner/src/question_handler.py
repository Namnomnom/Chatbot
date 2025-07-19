
from src.cli_handler import *
from src.chatbot import *
from src.command_handler import *
from src.csvdata_handler import *
from src.weather_forcast import *
import pandas as pd
import random
import logging
logger = logging.getLogger('chatbot') 

def possible_q(df):
    """ Print all possible questions from the dataframe 
    """
    print("Here are possible questions:")
    logger.info("Here are possible questions:")
    questions = df['Question']
    for question in questions:
        print(question)



def print_related_questions(input_text, questions_column, subject_column, answers_column, df):
    """
    Prints the related questions based on the input text and allows the user to select a question to display its answer.

    Args:
        input_text (str): The input text used to find related questions.
        questions_column (str): The column name in the dataframe that contains the questions.
        subject_column (str): The column name in the dataframe that contains the subject.
        answers_column (str): The column name in the dataframe that contains the answers.
        df (pandas.DataFrame): The dataframe containing the questions and answers.

    Returns:
        None
    """
    # get keyword all related questions rows from dataframe
    matching_rows_df = df[df[subject_column].str.lower() == input_text.lower()]
    
    
    if not matching_rows_df.empty:
        related_questions = matching_rows_df[questions_column].tolist()
        logger.info(related_questions)
        while True:
            
            #print all related questions
            
            for index, question in enumerate(related_questions):
                print(f"{index}. {question}")
            
            #get user input as question number
            
            selected_question_number = int(input("Enter the number of the questions list"))
            logger.info(selected_question_number)
            
            
            if 0 <= selected_question_number < len(related_questions):
                selected_question = related_questions[selected_question_number]
                selected_question_rows = df[df[questions_column] == selected_question]
                if not selected_question_rows.empty:
                    selected_answer = selected_question_rows[answers_column].iat[0]
                    
                    #if question input is event -> print weather + event
                    keyword_row_index = matching_rows_df.index[selected_question_number]
                    if keyword_of_question_is_event(keyword_row_index,'Subject','Answer',df):
                        logging.info('question input is event, printing event')
                        print(selected_answer)
                        weather_forecast = get_weather_forecast(selected_answer)
                        print(weather_forecast)
                        logger.info(selected_answer)
                        break
                    
                    # if question input is not event -> print answer
                    
                    else:
                        logger.info(selected_answer)
                        print(f"Answer: {selected_answer}")
                    break
            else:
                print("Invalid question number. Please enter a valid number.")
                logger.info(print("Invalid question number. Please enter a valid number."))

def print_random_answer(input_text, questions_column, questions_var_column, answers_column,answers_var_column,df):
    """
    Prints a random answer based on the input text.

    Args:
        input_text (str): The input text to search for in the questions column.
        questions_column (str): The column name containing the questions.
        questions_var_column (str): The column name containing the question variations.
        answers_column (str): The column name containing the answers.
        answers_var_column (str): The column name containing the answer variations.
        df (pandas.DataFrame): The DataFrame containing the data.

    Returns:
        str: The selected random answer.

    Raises:
        None

    """
    # get the row of the matching question
    matching_questions_df = df[(df[questions_column].str.lower() == input_text.lower()) | (df[questions_var_column].str.lower() == input_text.lower())]
    
    if not matching_questions_df.empty:
        
        # get the answers and answers variations
        related_answers = matching_questions_df[answers_column].tolist()
        answer_variations = matching_questions_df.iloc[0][answers_var_column]
        # get the answers variations
        if not pd.isna(answer_variations):
            variations = [var.strip() for var in answer_variations.strip('"').split('", "')]
            related_answers.extend(variations)
        
        # select a random answer
        
        if related_answers:
            selected_answer = random.choice(related_answers)
            logger.info(selected_answer)
            return selected_answer
        
        else:
            print("No answers found.")
            logger.info(print("No answers found."))


def is_question_or_variation(input_text, question_column, variation_column, df):
    """
    Checks if the input text is present in the question column or variation column of the given dataframe.

    Args:
        input_text (str): The input text to be checked.
        question_column (str): The name of the question column in the dataframe.
        variation_column (str): The name of the variation column in the dataframe.
        df (pandas.DataFrame): The dataframe to be checked.

    Returns:
        bool: True if the input text is found in either the question column or variation column, False otherwise.
    """
    #check if dataframe is empty or question column or variation column is not in dataframe
    
    if df.empty or question_column not in df.columns or variation_column not in df.columns:
        return False
    
    #check if input text is string
    
    if isinstance(input_text, str):
        input_text_lower = input_text.lower()
    else:
        return False
    
    # check if input text is in question column or variation column
    
    
    #get question column to list
    
    if input_text_lower in df[question_column].str.lower().values:
        return True
    
    #get variation column to list
    
    var_qst = []
    for variations in df[variation_column].apply(
            lambda x: str(x).strip('"').split('","') if not pd.isna(x) else []).values:
        var_qst.extend(variations)
    
    # check if input text is in variation column or question column
    
    if input_text_lower in map(str.lower, var_qst):
        return True
    return False


def is_keyword_or_variation(input_text, subject_column, subject_variation_column, df):
    """
    Checks if the input text is a keyword or a variation of a keyword in the given DataFrame.

    Parameters:
    input_text (str): The input text to check.
    subject_column (str): The column name in the DataFrame containing the keywords.
    subject_variation_column (str): The column name in the DataFrame containing the variations of keywords.
    df (pandas.DataFrame): The DataFrame to search for keywords and variations.

    Returns:
    bool: True if the input text is a keyword or a variation, False otherwise.
    """
    
    input_text_lower = input_text.lower()
    # check if input text is in subject column or subject variation column
    
    # check in subject column
    
    if input_text_lower in df[subject_column].str.lower().values:
        return True
    
    # check in subject variation column
    
    for variations in df[subject_variation_column]:
        if input_text_lower in str(variations).lower().split(', '):
            return True
    return False

def is_valid(df, question_row_index, keyword_column, answer_column):
    """
    Check if the given DataFrame is valid for processing.

    Args:
        df (pandas.DataFrame): The DataFrame to be checked.
        question_row_index (int): The index of the question row.
        keyword_column (str): The name of the keyword column.
        answer_column (str): The name of the answer column.

    Returns:
        bool: True if the DataFrame is valid, False otherwise.
    """
    if df.empty:
        return False
    if keyword_column not in df.columns or answer_column not in df.columns:
        return False
    if question_row_index < 0 or question_row_index >= len(df):
        return False
    return True

def keyword_of_question_is_event(question_row_index, keyword_column, answer_column, df):
    """
    Checks if the keyword of a question at the specified row index is 'event' or 'class'.

    Parameters:
    question_row_index (int): The row index of the question in the DataFrame.
    keyword_column (str): The column name of the keyword in the DataFrame.
    answer_column (str): The column name of the answer in the DataFrame.
    df (pandas.DataFrame): The DataFrame containing the questions and answers.

    Returns:
    bool: True if the keyword is 'event' or 'class', False otherwise.
    """
    #check if dataframe is valid
    
    if not is_valid(df, question_row_index, keyword_column, answer_column):
        return False
    
    #get keyword from dataframe
    
    keyword = df.iloc[question_row_index][keyword_column]
    
    #check if keyword is event or class
    
    return keyword in ['event', 'class']