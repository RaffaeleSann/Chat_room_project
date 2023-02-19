
import socket
import threading

#We want every user has a nickname
nickname = input("Choose your nickname : ").strip()
while not nickname:
    nickname = input("Your nickname should not be empty : ").strip()

#Creation of the socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = 'foo' # Insert the server IP
port = 8081

#We connect the socket to the server
my_socket.connect((host, port))

def thread_initial_sending():
    '''This function allows the client to send messages to the server'''
    # Wait for user to input a message
    condition = True
    while condition == True:
        req = (f'POST / HTTP/1.1\nmyline: connect\n\n{nickname}\nHELLO I WANT TO CONNECT WITH YOU\n')
        
        #message_with_nickname = f'POST / HTTP/1.1\nmy line:connect\n{nickname} >> {message_to_send}'
        if condition == True:
            my_socket.send(req.encode())
        condition = False

def thread_sending():
    while True:
        message = input()
        req = (f'POST / HTTP/1.1\nmyline: message to send\n\n{nickname}\n{message}\n')
        if message:
            my_socket.send(req.encode())


def thread_receiving():
    '''This function allows the client to receive messages from the server'''
    while True:
        message = my_socket.recv(1024).decode().splitlines()
        #print(message)
        print(message[-2],'->',message[-1])

thread_in_send = threading.Thread(target = thread_initial_sending)
thread_send = threading.Thread(target=thread_sending)
thread_receive = threading.Thread(target=thread_receiving)
thread_in_send.start()
thread_send.start()
thread_receive.start()