
import pandas as pd
import random

from bin.main import *
from src.question_handler import *
from src.cli_handler import *
from src.command_handler import *
from src.chatbot import *


def import_csv(df, csv_path, data_path):
    """
    Imports data from a CSV file and appends it to an existing DataFrame.
    
    Parameters:
        df (pandas.DataFrame): The existing DataFrame to which the CSV data will be appended.
        csv_path (str): The file path of the CSV file to import.
        data_path (str): The file path where the updated DataFrame will be saved.
        
    Returns:
        pandas.DataFrame: The updated DataFrame after importing the CSV data.
        
    Raises:
        FileNotFoundError: If the CSV file path is invalid and the file is not found.
        PermissionError: If there is insufficient access privilege rights to the CSV file.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file is corrupted or contains unsupported format.
        Exception: If any other error occurs during the CSV import process.
    """
    
    try:
        new_data = pd.read_csv(csv_path, encoding='latin1')
        df = pd.concat([df, new_data], ignore_index=True)
        df = df.sort_values(by='Subject')
        df.to_csv(data_path, index=False, encoding='latin1')
        print(f"CSV data from '{csv_path}' imported successfully.")
        return df
    except FileNotFoundError:
        print("Error: Invalid file path. File not found.")
    except PermissionError:
        print("Error: Insufficient access privilege rights. Permission denied.")
    except pd.errors.EmptyDataError:
        print("Error: Empty CSV file.")
    except pd.errors.ParserError:
        print("Error: Corrupted CSV file or unsupported format within CSV file.")
    except Exception as e:
        print(f"Error importing CSV: {e}")



def add_row_to_csv(df, questions, subjects, answers, data_path):
    """
    Adds a new row to a CSV file.

    Args:
        df (pandas.DataFrame): The DataFrame representing the CSV file.
        questions (list): A list of questions.
        subjects (list): A list of subjects.
        answers (list): A list of answers.
        data_path (str): The file path of the CSV file.

    Returns:
        pandas.DataFrame: The updated DataFrame.

    Raises:
        FileNotFoundError: If the file path is invalid and the file is not found.
        PermissionError: If there is insufficient access privilege rights and permission is denied.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file is corrupted or contains unsupported format.
        Exception: If any other error occurs while adding the row to the CSV file.
    """
    
    try:
        new_row = {'Question': questions[0], 'Subject': subjects[0], 'Answer': answers[0]}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(data_path, index=False, encoding='latin1')
        print("Row added to CSV file.")

    except FileNotFoundError:
        print("Error: Invalid file path. File not found.")
    except PermissionError:
        print("Error: Insufficient access privilege rights. Permission denied.")
    except pd.errors.EmptyDataError:
        print("Error: Empty CSV file.")
    except pd.errors.ParserError:
        print("Error: Corrupted CSV file or unsupported format within CSV file.")
    except Exception as e:
        print(f"Error adding row to CSV: {e}")

    return df

def find_question_row_index(input_text, question_column, variation_column, df):
    """
    Finds the row index of a question in a DataFrame based on the input text.

    Args:
        input_text (str): The input text to search for.
        question_column (str): The name of the column containing the questions.
        variation_column (str): The name of the column containing the question variations.
        df (pandas.DataFrame): The DataFrame to search in.

    Returns:
        tuple: A tuple containing a boolean value indicating if the question was found, and the row index of the question.
               If the question is not found, the boolean value is False and the row index is None.
    """
    input_text_lower = input_text.lower()
    #get all the variations of the question
    var_qst = []
    for variations in df[variation_column].apply(
            lambda x: str(x).strip('"').split('","') if not pd.isna(x) else []).values:
        var_qst.extend(variations)
    #check if the question is in the dataframe
    
    if input_text_lower in df[question_column].str.lower().values:
        question_indices = df[df[question_column].str.lower() == input_text_lower].index
        if len(question_indices) > 0:
            return True, question_indices[0]
    
    #check if the question variation is in the dataframe
    
    if input_text_lower in map(str.lower, var_qst):
        question_indices = df[df[variation_column].apply(
            lambda x: input_text_lower in str(x).lower() if not pd.isna(x) else False)].index
        if len(question_indices) > 0:
            return True, question_indices[0]
    
    return False, None



def remove_row_from_csv(df, questions, data_path):
    """
    Removes a row from a CSV file based on the given question.

    Args:
        df (pandas.DataFrame): The DataFrame representing the CSV file.
        questions (str): The question to be removed.
        data_path (str): The file path of the CSV file.

    Returns:
        pandas.DataFrame: The updated DataFrame after removing the row.

    Raises:
        FileNotFoundError: If the file path is invalid and the file is not found.
        PermissionError: If there is insufficient access privilege rights and permission is denied.
        pd.errors.EmptyDataError: If the CSV file is empty.
        pd.errors.ParserError: If the CSV file is corrupted or has an unsupported format.
        Exception: If there is an error removing the row from the CSV file.
    """
    try:
        is_question, question_index = find_question_row_index(questions, 'Question', 'Question_Variation', df)

        if is_question:
            df.drop(question_index, inplace=True)
            df.to_csv(data_path, index=False, encoding='latin1')
            print(f"Row with question '{questions}' removed from CSV file.")
        else:
            print(f"Question '{questions}' not found in the CSV file.")

    except FileNotFoundError:
        print("Error: Invalid file path. File not found.")
    except PermissionError:
        print("Error: Insufficient access privilege rights. Permission denied.")
    except pd.errors.EmptyDataError:
        print("Error: Empty CSV file.")
    except pd.errors.ParserError:
        print("Error: Corrupted CSV file or unsupported format within CSV file.")
    except Exception as e:
        print(f"Error removing row from CSV: {e}")

    return df


