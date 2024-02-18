# Yash Malik
# 2001CS79
# Tutorial 3

import socket
import sys
import threading

# Creating a socket
def CreateASocket():
    try:
        # Global Variables Declared
        global hostip # Stores the Host IP Address
        global portnumber # Stores the port number
        global s # Socket Object

        hostip = str(sys.argv[1]) # Taking cmd line input for values of host ip
        portnumber = int(sys.argv[2]) # Taking cmd line input for values of port number

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creating a socket
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
        global s # Socket Object

        print("Binding the Port: " + str(portnumber))
        s.bind((hostip, portnumber)) # Binding the Socket to the (Host, Port) Tuple
        s.listen(0)  # Putting the server in the Listening Mode

    except socket.error as msg:  # If Error arises in the above code
        print("Socket Binding Error: " + str(msg))  # Print Error message
        exit(0) # And Exit the program


# Establish Connection with a Client (NOTE: Client must be listening)
def SocketAccept():
    global address
    connection, address = s.accept() # Initiates a connection with the Client

    print("Connection has been established with IP " +
          address[0] + ":" + str(address[1]))

    # Creating new thread whenever a client connects
    t = threading.Thread(target=SendCommands, args=(connection, address,))
    t.start()


# Send Commands to a Client
def SendCommands(connection, address):
    msg = "Connection Established with the Server."
    connection.send(msg.encode())
    while True: # To keep receiving from Client until the connection closes
        data = connection.recv(1024)
        if not data:
            break
        expr = data.decode() # Data given in byte format need to be decoded
        answer = Calculate(expr)

        print("Equation received [" + expr + "] from " +
              address[0] + ":" + str(address[1]))
        output = str(answer)

        connection.send(output.encode())  # Sending data to the server
        print("Result sent to " + address[0] + ":" + str(address[1]))
    connection.close() # Closing the connection and the thread
    print("Connection has been closed with IP " +
      address[0] + ":" + str(address[1]))
        
# Calculator Function
def Calculate(expr):
    try:
        answer = eval(str(expr)) # eval() function of python calculates any arithmetic expression
    except:
        answer = "ERROR: Invalid Expression Entered"
    return answer

# The main function
def main():
    CreateASocket()
    BindSocket()
    while 1:  # So that another client can connect to our server after previous one has been closed
        SocketAccept()


if __name__ == "__main__":
    main()