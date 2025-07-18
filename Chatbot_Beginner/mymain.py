#our cod is executed  with : python mymain.py --action list  
#1.you can write and see answer(from csv file): ostfalia or wintersemster 
#2.you can write and see answer(from code): ostfalia? or wintersemester?
#3.you can write and see answer(from code and csv file): ostfali , wintersemester ( , is important and reoetitive question)
#4.you can write and see answer(from code): trivia (start QuizApp)
#5.you can write and see answer: clausthal event (from csv file. )
#6.you can write and see answer: weather in berlin (current weather Berlin from webseit) : clausthal event (from csv file)
#7.you can write and see answer: exit (end programm)  


#add question and answer ( CSV file)
#python mymain.py --action add --question "New Question?" --answer "New answer in row Answer1;New answer in row Answer2"

#remove question and row ( CSV file) 
#python mymain.py --action remove --question "which Question to Remove?"
#python mymain.py --action remove --row 2  

#read list ( CSV file)
#python mymain.py --action list

#for error
#python mymain.py --action add --question "New Question?" --answer "New Answer1::New Answer2"
#python read_log.py
#python mymain.py --debug
   
  

import datetime
import random
import argparse
import os
import logging
import pandas as pd
import requests




class QuizApp:
    def __init__(self):
        self.quiz_started = False
        self.questions_asked = 0
        self.correct_answers = 0
        self.quiz_questions = [
            {"question": "Was ist die Hauptstadt von Frankreich?", "options": ["Berlin", "Paris", "Rom"], "correct": "Paris"},
            {"question": "Wie viele Planeten hat unser Sonnensystem?", "options": ["7", "8", "9"], "correct": "8"},
            {"question": "Was ist die größte Säugetierart?", "options": ["Elefant", "Blauwal", "Giraffe"], "correct": "Blauwal"},
            {"question": "Wie viele Kontinente gibt es auf der Erde?", "options": ["5", "6", "7"], "correct": "7"},
            {"question": "Wer schrieb 'Romeo und Julia'?", "options": ["Charles Dickens", "William Shakespeare", "Jane Austen"], "correct": "William Shakespeare"},
            {"question": "Wie viele Beine hat eine Spinne?", "options": ["6", "8", "10"], "correct": "8"},
            {"question": "Welches Element hat das chemische Symbol 'O'?", "options": ["Sauerstoff", "Gold", "Eisen"], "correct": "Sauerstoff"},
            {"question": "In welchem Jahr fand die Erste Mondlandung statt?", "options": ["1965", "1969", "1975"], "correct": "1969"},
            {"question": "Was ist die Hauptzutat in Guacamole?", "options": ["Tomate", "Avocado", "Zwiebel"], "correct": "Avocado"},
            {"question": "Wer malte die Mona Lisa?", "options": ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso"], "correct": "Leonardo da Vinci"}
        ]

    def start_quiz(self):
        self.quiz_started = True
        self.questions_asked = 0
        self.correct_answers = 0
        random.shuffle(self.quiz_questions)
        return self.ask_question(), False
    
    def process_input(self, user_input):
        if self.quiz_started:
            return self.process_quiz_input(user_input)
        elif "trivia" in user_input.lower():    
            #self.start_quiz() 
            return self.ask_question(), False
        return "Nicht verstanden. Um das Quiz zu starten, schreibe 'Trivia'.", False

    def ask_question(self):
        current_question = self.quiz_questions[self.questions_asked]
        options = ", ".join(current_question["options"])
        progress = "Frage {} von {}; Punktestand {}/{}".format(
            self.questions_asked + 1, len(self.quiz_questions), self.correct_answers, self.questions_asked)
        return "{}\n{}\n{}".format(progress, current_question["question"], options)

        # Process user input for the quiz
    def process_quiz_input(self, user_input):
        current_question = self.quiz_questions[self.questions_asked]
        if user_input.lower() == current_question["correct"].lower():
            self.correct_answers += 1
            response = "Richtig! "
        else:
            response = "Falsch! "
        response += "Die richtige Antwort ist {}. ".format(current_question["correct"])
        self.questions_asked += 1
        if self.questions_asked < len(self.quiz_questions):
            return response + "\n" + self.ask_question(), False
        else:
            final_message = response + "\nQuiz beendet! Du hast {} von {} Fragen richtig beantwortet.".format(self.correct_answers, len(self.quiz_questions))
            self.quiz_started = False
            return final_message, True



#function for current weather 
def get_current_weather(location, api_key):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={location}&appid={api_key}&units=metric"  # 'units=metric' for Celsius

    response = requests.get(complete_url)
    if response.status_code == 200:
        weather_data = response.json()
        weather_description = weather_data['weather'][0]['description']
        temperature = weather_data['main']['temp']
        return f"{weather_description}, {temperature}°C"
    else:
        return "Weather data not available."   

#function for time
def ermittelZeit():
    VarActualTime = datetime.datetime.now()
    currentTimeString = VarActualTime.strftime("%H:%M:%S")
    return currentTimeString

#function for add question in csv file
def add_question(df, question, answers):
    new_row = [question] + [answer.strip() for answer in answers.split('::')]

    # Make sure the new row has the same number of elements as the DataFrame columns
    if len(new_row) == len(df.columns):
        df.loc[len(df)] = new_row
    else:
        logging.error("Mismatched number of elements in the new row. Please check the input.")

#function for remove question from csv file
def remove_question(df, question):
    df = df[df['Question'] != question]
    df = df.reset_index(drop=True)
    return df

#function for record changes
def save_dataframe(df, filename):
    df.to_csv(filename, index=False, sep=';')


def create_timestamped_filename(prefix, extension):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"

#function for find random answer
def get_random_answer(answer_list):
    return random.choice(answer_list)

#function for read csv and error
def handle_csv_import_errors(file_path):
    try:
        return pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    except FileNotFoundError as e:
        logging.error(f"Error: File '{file_path}' not found - {e}")
        return None
    except PermissionError as e:
        logging.error(f"Error: Insufficient access privilege for file '{file_path}' - {e}")
        return None
    except pd.errors.EmptyDataError as e:
        logging.error(f"Error: File '{file_path}' is empty - {e}")
        return None
    except pd.errors.ParserError as e:
        logging.error(f"Error: Failed to parse CSV file '{file_path}'. Check if the file is corrupted - {e}")
        return None
    except Exception as e:
        logging.error(f"Error: An unexpected error occurred - {e}")
        return None


#Start main function and input question from user and search in csv file, code or weather
def main():
    #API from website (https://home.openweathermap.org/api_keys)
    api_key = "7fe4ba1a3e3bcb899183edc7847f21d5"

    #opration add, remove, list
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", choices=["add", "remove", "list"], required=True, help="Action to perform")
    parser.add_argument("--question", help="Question to add or remove")
    parser.add_argument("--answer", help="Answer to add")
    parser.add_argument("--row", type=int, help="Row number to remove")
    args = parser.parse_args()
    
    #logging
    log_filename = create_timestamped_filename("script_log", "txt")
    logging.basicConfig(filename=log_filename, level=logging.ERROR)
    csv_file_path = 'Prokekt^N7.csv'
    df = handle_csv_import_errors(csv_file_path)
    if df is None:
        return


    try:
        if args.action == "add":
            if args.question and args.answer:
                add_question(df, args.question, args.answer)
            else:
                logging.error("Error: Both --question and --answer are required for 'add' action.")
        elif args.action == "remove":
            if args.question:
                df = remove_question(df, args.question)
            elif args.row is not None:
                df = df.drop(args.row)
            else:
                logging.error("Error: Either --question or --row is required for 'remove' action.")
        elif args.action == "list":
            print(df)

        # Save the modified DataFrame back to CSV
        save_dataframe(df, csv_file_path)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


    
    quiz_app = QuizApp()
    asked_questions = set()  # Set to keep track of asked questions
    print(ermittelZeit(), "Hallo")


    #question and answer in code
    known_answers = {
        "ostfalia?": ["0.wie viele studierende hat die ostfalia?", "1.wie viele standorte hat die ostfalia?",
                      "2.wo befindet sich das hauptgebäude der ostfalia?", "3.wann sind die öffnungszeiten der ostfalia?"],
        "wintersemester?": ["0.Welche Studiengänge werden im Wintersemester an der Ostfalia angeboten?",
                            "1.Gibt es besondere Veranstaltungen während des Wintersemesters an der Ostfalia?",
                            "2.Wie unterstützt die Ostfalia ihre Studierenden im Wintersemester?",
                            "3.Welche Aktivitäten plant die Studentenvereinigung für das kommende Wintersemester an der Ostfalia?"],
    }
    answer11 = {
        "ostfalia?": ["0.Die Ostfalia Hochschule hat zur Zeit rund 15.000 Studierende",
                      "1.jeweils in Wolfsburg, Wölfenbüttel, Braunschweig und Salzgitter",
                      "2.Salzdahlumer Str. 46/48 Gebäude D - EG Raum D001",
                      "3.Mo-Fr: 07:00 Uhr -19:00 Uhr (Zutritt ohne Ostfalia-Card)"],
        "wintersemester?": ["0.Die Dokumente liegen im PDF-Format (Portable Document Format) vor.",
                            "1.ja, sie können in diesem Links finden https://www.ostfalia.de/cms/de/h/fakultaet/veranstaltungen/",
                            "2.Wir können Ihnen mit diesem Links helfen https://www.ostfalia.de/cms/de/i/studium/ablauf-des-studiums---hilfe/",
                            "3.Hier stellen sich auch die verschiedenen Studierendeninitiativen und Einrichtungen der Ostfalia am Campus Wolfsburg vor.https://www.ostfalia.de/cms/de/campus/wob/infos-fuer-erstsemester-ss2022/ "]
    }


   #chech the user's question
    while True:
        user_input = input("Ask me something: ").lower()
        if user_input == 'exit':
             break  # Exit the main loop and end the program
        if "trivia" in user_input:
            response, quiz_ended = quiz_app.start_quiz()  # Start the quiz and get the first question
            print(response)
            while not quiz_ended:
                user_input = input("Which answer is correct?: ").lower()
                response, quiz_ended = quiz_app.process_input(user_input)
                print(response)

               
         
         # Example usage weather
        if "weather" in user_input:  # Example condition to fetch weather
            api_key == "7fe4ba1a3e3bcb899183edc7847f21d5"
            location = "Berlin"  # You might want to extract location from user_input
            current_weather = get_current_weather(location, api_key)
            print("Current weather in {}: {}".format(location, current_weather))
            continue
        
        # search for 2 questions
        user_questions = user_input.split(',')
        for user_question in user_questions:
            user_question = user_question.strip()
            
            
             # Repeat the logic to show the answer again
            if user_question in asked_questions:
                print("This question has already been asked.")


            elif user_question in known_answers:
                print(ermittelZeit(), known_answers[user_question])
                user_question2 = int(input("Enter the question number: "))
                if user_question2 < len(known_answers[user_question]):
                    print(ermittelZeit(), answer11[user_question][user_question2])
                else:
                    print(ermittelZeit(), "Invalid index.")
                asked_questions.add(user_question)  # Add to the set of asked questions


            else:
                found = False
                for index, row in df.iterrows():
                    if user_question == row['Question'].lower():
                        print(f"{ermittelZeit()}, {row['Question']}")
                        selected_answer = random.choice([row['Answer1'], row['Answer2']])
                        print(f"Answer: {selected_answer}")
                        found = True
                        asked_questions.add(user_question)  # Add to the set of asked questions

                        break
                if not found:
                    print(ermittelZeit(), "Question not found.")

        if user_input == 'exit':
           break  # Exit the main loop and end the program






if __name__ == "__main__":
    main()
