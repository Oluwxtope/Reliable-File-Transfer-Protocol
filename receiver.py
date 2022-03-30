from socket import *

# handle program startup, request inputs from user
info = input("Enter the UDP port number to receive data, drop probability, and name of the file received data will be written: ")
info = info.split(" ")
host_address = str(info[0])
send_port = int(info[1])
receive_port = int(info[2])
time_out = int(info[3])
file_name = str(info[4])