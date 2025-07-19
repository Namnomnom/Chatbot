from src.chatbot import *

import logging
import pandas as pd
import logging
from datetime import datetime
logger = logging.getLogger('chatbot')  

trivia_questions = [
    {
        "question": "What is the largest planet in our solar system?",
        "options": ["A) Mars", "B) Jupiter", "C) Earth", "D) Saturn"],
        "answer": ["B", "Jupiter"]
    },
    {
        "question": "In which year did the Titanic sink?",
        "options": ["A) 1912", "B) 1923", "C) 1905", "D) 1931"],
        "answer": ["A", "1912"]
    },
    {
        "question": "Who wrote the play 'Romeo and Juliet'?",
        "options": ["A) Charles Dickens", "B) William Shakespeare", "C) Jane Austen", "D) Mark Twain"],
        "answer": ["B", "William Shakespeare"]
    },
    {
        "question": "What is the capital city of Japan?",
        "options": ["A) Beijing", "B) Tokyo", "C) Seoul", "D) Bangkok"],
        "answer": ["B", "Tokyo"]
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": ["A) Oxygen", "B) Gold", "C) Iron", "D) Sodium"],
        "answer": ["A", "Oxygen"]
    },
    {
        "question": "In what year did the first manned moon landing occur?",
        "options": ["A) 1969", "B) 1975", "C) 1982", "D) 1958"],
        "answer": ["A", "1969"]
    },
    {
        "question": "What is the largest mammal in the world?",
        "options": ["A) Elephant", "B) Blue Whale", "C) Giraffe", "D) Polar Bear"],
        "answer": ["B", "Blue Whale"]
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A) Vincent van Gogh", "B) Pablo Picasso", "C) Leonardo da Vinci", "D) Michelangelo"],
        "answer": ["C", "Leonardo da Vinci"]
    },
    {
        "question": "What is the currency of Australia?",
        "options": ["A) Euro", "B) Dollar", "C) Pound", "D) Yen"],
        "answer": ["B", "Dollar"]
    },
    {
        "question": "Which planet is known as the 'Red Planet'?",
        "options": ["A) Venus", "B) Mars", "C) Mercury", "D) Jupiter"],
        "answer": ["B", "Mars"]
    }
]

def init_trivia():
    logger.info("Welcome to the trivia game!")
    print("Welcome to the trivia game!")
    i = 0
    score = 0
    for question in trivia_questions:
        logger.info(f"Question {i+1} / 10:")
        print(f"Question {i+1} / 10:")
        logger.info(f"{question['question']}")
        print(f"{question['question']}")
        logger.info("Options:")
        print("Options:")
        options_str = " ".join(question["options"])
        logger.info(options_str)
        print(options_str)
        logger.info("Answer:")
        print("Answer:")
        
        user_answer = input()
        i += 1
        if user_answer in question["answer"][1] or user_answer in question["answer"][0]:
            logger.info("Correct!")
            print("Correct!")
            score += 1
        
        elif user_answer.lower() == "score":
            print(f"Your score is {score}/10.")
            logger.info("User asked for score")
            logger.info(f"Your score is {score}/10.")
            continue
        elif user_answer.lower() == "trivia":
            logger.info("Thank you for playing!")
            logger.info(f"Your score is {score}/10.")
            print("Thank you for playing!")
            print(f"Your score is {score}/10.")
            break
        elif user_answer.lower() not in question["answer"]:
            logger.info("Incorrect!")
            print("Incorrect!")

        logger.info(f"Your score is {score}/10.")
        print(f"Your score is {score}/10.")
        