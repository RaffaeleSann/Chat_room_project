import socket
import threading

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 8081
ADDRESS = ''

#the idea behind this list is to fill it with the users enjoying the chat
#so when someone sends a message, the server sends this message to everyone in this list except the original sender
broadcast_list = []   

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
my_socket.bind((ADDRESS, PORT))

def accept_loop():
    while True:
        #The listen() method just allows incoming connections. The accept() method return a tuple, the first element is the connection, 
        # we will now use it to interact with the client 
        # and the second one is a tuple containing the IP address of the client as well as the port used (it can be different from the port you set up).
        my_socket.listen()
        client, client_address = my_socket.accept()
        #welcome(client)
        #number_members_discl(client,broadcast_list)
        broadcast_list.append(client)
        start_listening_thread(client)

#  def welcome(client):
#     '''Send greetings to the yet arrived'''
#     listen_thread()
#     user_name = message[33:req.rfind('H')]
#     greetings = f'Hello {user_name}\nNice to meet you!\n'
#     client.send(greetings.encode())


def number_members_discl(client,broadcast_list):
    '''Tells to the upcoming user how many are connected yet'''
    if len(broadcast_list)>1:
        num_memb = f'{len(broadcast_list)} users connected yet\n'
        client.send(num_memb.encode())
    elif len(broadcast_list)==1:
        mem = f'1 user connected yet\n'
        client.send(mem.encode())
    else:
        no_one_discl = "There's no one in the chat room\n"
        client.send(no_one_discl.encode())
        
def start_listening_thread(client):
    '''It allows the server to listen the client in order to receive his messages'''
    client_thread = threading.Thread(
            target=listen_thread,
            args=(client,) #the list of argument for the function
        )
    client_thread.start()
    
def listen_thread(client):
    while True:
        #The recv() method takes only one non-optional argument, the buffer size, that is the max space available to receive the message.
        # Don’t forget that this method returns a byte object and so we need to decode it into a string.
        message = client.recv(1024).decode().splitlines()
        protocollo_iniziale = 'myline: connect'
        user_name = message[-2]
        user_name_strip = user_name.strip()
        if message:
            if protocollo_iniziale in message:
                print(message[-2],'->',message[-1])
                #user_name = message[-2]
                #user_name_strip = user_name.strip()
                #print(user_name, user_name_strip)
                welcome_response = f'GET / HTTP/1.1 200 OK\nmyline: connect\n\nHELLO {user_name_strip}\nNICE TO MEET YOU'
                #welcome_response_to_send = welcome_response[welcome_response.find('HELLO'):]
                client.send(welcome_response.encode())
            else:
                print(message[-2],'->',message[-1])
                mess_accept = f'GET / HTTP/1.1 200 OK\nmyline: message to send\n\nMESSAGE ACCEPTED FOR DELIVERY'
                client.send(mess_accept.encode())
                broadcast(message,user_name_strip,client)
        else:
            print(f"client has been disconnected : {client}")
            return
        
def broadcast(message,user_name_strip,sender):
    '''Send the message (message) to every member of the broadcast_list'''
    for client in broadcast_list:
        if client!=sender:
            try:
                #user_name_strip_len = len(user_name_strip)
                message_to_send = message[-1]
                mess_http = f'GET / HTTP/1.1 200 OK\nmyline: message to receive\n\nFROM {user_name_strip}:\n{message_to_send}'
                client.send(mess_http.encode())
            except:
                broadcast_list.remove(client)
                print(f"Client removed : {client}")

accept_loop()