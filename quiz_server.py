import socket
import threading
import random

# Define the IP Address and Port number
IP = "127.0.0.1"
PORT = 1234

# List to maintain all the clients
clients = []

# Questions and Answers
questions = [
    "Question 1: What is the capital of France?",
    "Question 2: Who painted the Mona Lisa?",
    "Question 3: What is the largest planet in our solar system?",
    "Question 4: What is the chemical symbol for gold?",
    "Question 5: Which country won the 2018 FIFA World Cup?",
]

answers = [
    "Paris",
    "Leonardo da Vinci",
    "Jupiter",
    "Au",
    "France",
]

def get_random_question_answer(conn):
    random_index = random.randint(0, len(questions) - 1)
    random_question = questions[random_index]
    random_answer = answers[random_index]
    conn.send(random_question.encode('utf-8'))
    return random_index, random_question, random_answer

def remove_question(index):
    questions.pop(index)
    answers.pop(index)

def client_thread(conn):
    score = 0
    conn.send("Welcome to the quiz game!\n".encode('utf-8'))
    conn.send("Instructions: Answer each question with the correct answer.\n".encode('utf-8'))

    while True:
        data = conn.recv(1024).decode('utf-8')
        if not data:
            clients.remove(conn)
            break

        if data.strip().lower() == current_answer.lower():
            score += 1
            conn.send("Correct answer! Your score is now {}.\n".format(score).encode('utf-8'))
            remove_question(current_index)
            current_index, current_question, current_answer = get_random_question_answer(conn)
        else:
            conn.send("Incorrect answer. Try again!\n".encode('utf-8'))
            current_index, current_question, current_answer = get_random_question_answer(conn)

    conn.close()

# Create the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the server to the IP and Port
server_socket.bind((IP, PORT))

# Listen for incoming requests
server_socket.listen()

print("Quiz server is running on {}:{}".format(IP, PORT))

while True:
    conn, addr = server_socket.accept()
    clients.append(conn)
    threading.Thread(target=client_thread, args=(conn,)).start()
