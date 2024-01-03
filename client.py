import socket
import tkinter as tk

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Client's host and port
host = '127.0.0.1'
port = 12345

client_socket.connect((host, port))
response = client_socket.recv(1024).decode()

'''
message = ""

def get_message():
    message = "".join([entry.get() for entry in otp_entries])
    clear_entries()

# Function to clear the entry boxes
def clear_entries():
    for entry in otp_entries:
        entry.delete(0, tk.END)
        
root = tk.Tk()
root.title("Master Mind Game")

entries = []
for i in range(5):
    entry = tk.Entry(root, width=5)
    entry.grid(row=0, column=i)
    entries.append(entry)
    '''

if response == "Start Game!!!":
    while True:
        while True:
            '''
            button = tk.Button(root, text="submit", command=get_message)
            button.grid(row=1, columnspan=5)
            
            '''
            message = input("Enter a guess (or type 'exit' to end the conversation): ")

            if len(message) != 5 and message!="exit":
                print("Invalid entry. Try again.")
            else:
                break

        if message.lower() == 'exit':
            client_socket.send(message.encode())
            break
        else:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                print("An error occurred when sending data to the server: ", e)
                client_socket.close()
                exit(1)

            response = client_socket.recv(1024).decode()
            print("Server response: ", response)

            if 'X' not in response and '-' not in response:
                print("Congratulations! The code word is ", response)
                break
else:
    print(response)

#root.mainloop()
client_socket.close()
