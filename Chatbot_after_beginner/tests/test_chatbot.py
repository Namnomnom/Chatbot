import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
from src.chatbot import Chatbot
from src.command_handler import *
from src.csvdata_handler import *
from src.question_handler import *
import pandas as pd
class TestChatbot(unittest.TestCase):
    def setUp(self):
        args_mock = MagicMock()
        data_file = '/chatbotdata_test.csv'
        self.chatbot = Chatbot(data_file, args_mock)
        self.df = pd.DataFrame({
            'Subject': ['courses','courses', 'admissions'],
            'Subject_Variation': ['study progrmmes, degree programmes,majors','study progrmmes, degree programmes,majors', 'inscription'],
            'Question': ['What majors are offered at Ostfalia?', 'Can you tell me about the Computer Science program at Ostfalia?','How do I apply to Ostfalia Uni?'],
            'Question_variation': ['', '', ''],
            'Answer': ['Ostfalia University offers a variety of majors, including Business Administration, Engineering, and Social Sciences. Check our website for a complete list of available majors.','The Computer Science program at Ostfalia covers topics such as algorithms, data structures, and software development. For specific details, please refer to the course catalog on our website.','To apply to Ostfalia University, you need to visit our official admissions portal and follow the application instructions.'],
            'Answer_Variation': ['', '', ''],
        })
        
    @patch('builtins.input', return_value='--importcsv "import_test.csv"')
    def test_import_csv(self, mock_input):
        print("Testing import_csv")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            csv_path = 'mport_test.csv'
            data_path='chatbotdata_test.csv'
            import_csv(self.df, csv_path, data_path)
            print("Captured stdout:", mock_stdout.getvalue())



if __name__ == '__main__':
    unittest.main()

