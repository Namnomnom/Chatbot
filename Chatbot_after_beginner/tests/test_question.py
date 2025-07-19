import unittest
from io import StringIO
from unittest.mock import MagicMock, patch

from src.chatbot import Chatbot
from src.command_handler import *
from src.csvdata_handler import *
from src.question_handler import *
import pandas as pd



class TestQuestion(unittest.TestCase):
    def setUp(self):
        args_mock = MagicMock()
        data_file = '/chatbotdata_test.csv'
        self.chatbot = Chatbot(data_file, args_mock)
        self.df = pd.DataFrame({
            'Subject': ['courses','courses', 'admissions'],
            'Subject_Variation': ['study progrmmes, degree programmes,majors','study progrmmes, degree programmes,majors', 'inscription'],
            'Question': ['What majors are offered at Ostfalia?', 'Can you tell me about the Computer Science program at Ostfalia?','How do I apply to Ostfalia Uni?'],
            'Question_Variation': ['', '', ''],
            'Answer': ['Ostfalia University offers a variety of majors Check our website.','The CS program at Ostfalia covers many topics refer to the course catalog on our website.','To apply to Ostfalia University, you need to visit our official admissions portal and follow the application instructions.'],
            'Answer_Variation': ['random answer', 'random answer', 'random answer'],
        })

    
    @patch('builtins.input', return_value='1')
    def test_print_related_questions(self, mock_input):
        expected_output = "0. What majors are offered at Ostfalia?\n1. Can you tell me about the Computer Science program at Ostfalia?\nAnswer: The CS program at Ostfalia covers many topics refer to the course catalog on our website.\n"
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_related_questions('courses', 'Question', 'Subject', 'Answer', self.df)
            self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    def test_possible_q(self):
        expected_output = "Here are possible questions:\nWhat majors are offered at Ostfalia?\nCan you tell me about the Computer Science program at Ostfalia?\nHow do I apply to Ostfalia Uni?\n"            
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            possible_q(self.df)
            self.assertEqual(mock_stdout.getvalue(), expected_output)

    
    
    
    @patch('builtins.input', return_value='0')
    def test_print_related_questions_selected_question(self, mock_input):
        expected_output = "0. What majors are offered at Ostfalia?\n1. Can you tell me about the Computer Science program at Ostfalia?\nAnswer: Ostfalia University offers a variety of majors Check our website.\n"
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            print_related_questions('courses', 'Question', 'Subject', 'Answer', self.df)
            self.assertEqual(mock_stdout.getvalue(), expected_output)
    
    

    @patch('builtins.input', return_value='0')
    def test_print_random_answer(self, mock_input):
        expected_output = ['Answer: To apply to Ostfalia University, you need to visit our official admissions portal and follow the application instructions.','random answer','To apply to Ostfalia University, you need to visit our official admissions portal and follow the application instructions.']
        with patch('sys.stdout', new_callable=StringIO):
            actual_output=print_random_answer('How do I apply to Ostfalia Uni?', 'Question', 'Question_Variation','Answer_Variation' ,'Answer', self.df)
            print("Actual output:", actual_output)
            self.assertIn(actual_output, expected_output)
            
            
   
    def test_is_question_or_variation(self):
        self.assertTrue(is_question_or_variation('Can you tell me about the Computer Science program at Ostfalia?', 'Question', 'Question_Variation', self.df))
        self.assertTrue(is_question_or_variation('How do I apply to Ostfalia Uni?', 'Question', 'Question_Variation', self.df))
        self.assertFalse(is_question_or_variation('How are you?', 'Question', 'Question_Variation', self.df))
        self.assertFalse(is_question_or_variation('Test me false?', 'Question', 'Question_Variation', self.df))
    
       
    def test_find_question_row_index(self):
        input_text = 'How do I apply to Ostfalia Uni?'
        question_column = 'Question'
        variation_column = 'Question_Variation'
        result, index = find_question_row_index(input_text, question_column, variation_column, self.df)
        self.assertTrue(result)
        self.assertEqual(index, 2)

        input_text = 'Can you tell me about the Computer Science program at Ostfalia?'
        result, index = find_question_row_index(input_text, question_column, variation_column, self.df)
        self.assertTrue(result)
        self.assertEqual(index, 1)

        input_text = 'Nonexistent question'
        result, index = find_question_row_index(input_text, question_column, variation_column, self.df)
        self.assertFalse(result)
        self.assertIsNone(index)


if __name__ == '__main__':
    unittest.main()
