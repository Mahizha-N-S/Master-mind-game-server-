import socket
import threading

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server's host and port
host = '127.0.0.1'
port = 12345

code_length = 5
max_attempts = 10  # Maximum number of attempts allowed
client_limit = 3  # Maximum number of clients allowed

# Shared data structure to hold game-related information
class GameData:
    def __init__(self):
        self.code = ""
        self.attempts = 0
        self.game_over = False

game_data = GameData()

# Semaphore for synchronization
mutex = threading.Semaphore(1)

def choose_code():
    while True:
        code = str(input("Enter a 5-letter code to be guessed: "))

        if len(code) == code_length:
            break
        print("Invalid. Try again.")

    return code.upper()

def check_code(response):
    hint = ""

    code_copy = game_data.code
    for i in range(0, code_length):
        if response[i] == game_data.code[i]:
            hint += game_data.code[i]
            code_copy = code_copy.replace(game_data.code[i], '', 1)
        elif response[i] in code_copy:
            hint += 'X'
            code_copy = code_copy.replace(response[i], '', 1)
        else:
            hint += '-'

    return hint

def handle_client(client_socket):
    with mutex:
        game_data.attempts += 1

    while not game_data.game_over and game_data.attempts <= max_attempts:
        data = client_socket.recv(1024).decode()
        if not data:
            break

        response_data = data.upper()

        if response_data == 'EXIT':
            break
        elif len(response_data) != 5:
            print("Invalid entry")
            break

        hint = check_code(response_data)
        client_socket.send(hint.encode())

        if hint.upper() == game_data.code:
            print("Code word guessed.")
            game_data.game_over = True

    # Close the client socket
    client_socket.close()

    #active_clients.remove(threading.current_thread())

if __name__ == '__main__':
    code = choose_code()
    game_data.code = code

    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Server is listening for incoming connections...")
    print("Port number:", port)

    current_clients = 0
    #active_clients = []

    while not game_data.game_over:
        if current_clients < client_limit:
            client_socket, client_address = server_socket.accept()
            print("Connection from ", client_address, " established.")
            client_socket.send("Start Game!!!".encode())
            current_clients += 1

            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

            #active_clients.append(client_thread)
        else:
            client_socket, client_address = server_socket.accept()
            print(f"Server is busy. Connection from ", client_address, " declined.")
            client_socket.send("Server is busy. Please try again later.".encode())
            client_socket.close()

    if game_data.game_over:
        client_socket.send("Game over. Word Guessed".encode())

    if game_data.attempts >= max_attempts:
        client_socket.send("Maximum attempts reached. Game over.".encode())
        client_socket.close()

