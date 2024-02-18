# Yash Malik
# 2001CS79
# Tutorial 3

import socket
import sys

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostip = sys.argv[1]  # taking input as command line arguement
portnumber = int(sys.argv[2])

c.settimeout(1)

try:
    c.connect((hostip, portnumber))  # connects to the server
    print("Trying to Connect to Server.")
    try:
        msg = c.recv(1024)
        print(msg.decode())
        while True:  # until user sends a 'N'
            inp = input("Please enter the message to the server: ")
            c.send(inp.encode())
            answer = c.recv(1024)
            print("Server replied: " + answer.decode())
            inp = input("Do you wish to continue? Y/N\n")
            if (inp == "N"):
                break
    except socket.timeout:
        print("Server Busy Try Again!")
        c.close()
except socket.error as message:
    print("Socket Connection Error: " + str(message))

# print(x)


c.close()
