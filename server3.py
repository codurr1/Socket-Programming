# Yash Malik
# 2001CS79
# Tutorial 3

import socket
import sys
import select
import queue


input_sockets = []  # Sockets to be read from
output_sockets = []  # Sockets to be written to
message_queues = {}  # Outgoing message queues for each socket
client_addresses = {}  # Mapping socket's connection to its address

# Creating a socket
def CreateASocket():
    try:
        # Global Variables Declared
        global hostip # Stores the Host IP Address
        global portnumber # Stores the port number
        global server # Socket Object

        hostip = str(sys.argv[1]) # Taking cmd line input for values of host ip
        portnumber = int(sys.argv[2]) # Taking cmd line input for values of port number

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a socket
        # socket.AF_INET refers to the address family IPv4
        # socket.SOCK_STREAM means connected oriented TCP protocol

    except socket.error as msg: # If Error arises in the above code
        print("Socket Creation Error: " + str(msg)) # Print Error message
        exit(0) # And Exit the program

# Binding the Socket and Listening for Connections
def BindSocket():
    try:
        # Accessing Global Variables
        global hostip # Stores the Host IP Address
        global portnumber # Stores the port number
        global server # Socket Object

        print("Binding the Port: " + str(portnumber))
        server.bind((hostip, portnumber)) # Binding the Socket to the (Host, Port) Tuple
        server.listen(0)  # Putting the server in the Listening Mode
        
        
        input_sockets.append(server) # Appending each new socket object to input

    except socket.error as msg:  # If Error arises in the above code
        print("Socket Binding Error: " + str(msg))  # Print Error message
        exit(0) # And Exit the program


# Establish Connection with a Client (NOTE: Client must be listening)
def SocketAccept(server):
    global address
    connection, address = server.accept() # Initiates a connection with the Client
    

    msg = "Connection Established with the Server."

    connection.send(msg.encode())
    print("Connection has been established with IP " +
          address[0] + ":" + str(address[1]))
    client_addresses[connection] = address
    return connection


def ResultGeneration(connection, data):
    address = client_addresses[connection]
    expr = data.decode()  # decode from byte
    answer = str(Calculate(expr))
    print("Equation received [" + expr + "] from " +
          address[0] + ":" + str(address[1]))
    return answer


def SendResult(connection, result):
    address = client_addresses[connection]
    connection.send(result.encode())  # encode to byte
    print("Result sent to " + address[0] + ":" + str(address[1]))


def CloseConnection(connection):
    address = client_addresses[connection]
    connection.close()
    print("Connection has been closed with " +
          address[0] + ":" + str(address[1]))


# Calculator Function
def Calculate(expr):
    try:
        answer = eval(str(expr)) # eval() function of python calculates any arithmetic expression
    except:
        answer = "ERROR: Invalid Expression Entered"
    return answer


def ChooseSocket():
    while input_sockets:
        readable, writable, exceptional = select.select(
            input_sockets, output_sockets, input_sockets)
        # select() returns three new lists, containing subsets of the contents of the lists passed in. 
        # All of the sockets in the readable list have incoming data buffered and available to be read. 
        # All of the sockets in the writable list have free space in their buffer and can be written to. 
        # The sockets returned in exceptional have had an error

        for s in readable:  # contains list of sockets available to be read
            if s is server:  # ready to accept incoming connection
                connection = SocketAccept(s)
                connection.setblocking(0)
                # adding the new connection to the list of input_sockets to monitor
                input_sockets.append(connection)
                message_queues[connection] = queue.Queue()
            else:
                data = s.recv(1024)
                if data:  # data sent from an established connection
                    result = ResultGeneration(s, data)
                    message_queues[s].put(result)
                    if s not in output_sockets:
                        output_sockets.append(s)
                else:  # client has disconnected
                    CloseConnection(s)
                    if s in output_sockets:
                        output_sockets.remove(s)
                    input_sockets.remove(s)
                    del client_addresses[s]
                    del message_queues[s]

        for s in writable:
            try:
                next_message = message_queues[s].get_nowait()
            except queue.Empty:
                # so that select() does not indicate that the socket is ready to send data
                output_sockets.remove(s)
            else:
                SendResult(s, next_message)

        for s in exceptional:  # if there is an error with a socket
            CloseConnection(s)
            input_sockets.remove(s)
            if s in output_sockets:
                output_sockets.remove(s)
            del client_addresses[s]
            del message_queues[s]


# The main function
def main():
    CreateASocket()
    BindSocket()
    ChooseSocket()

if __name__ == "__main__":
    main()
