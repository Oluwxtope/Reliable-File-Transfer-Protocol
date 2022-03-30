from socket import *

# request input from user
info = input("Enter the host address of the receiver, port number to used to send data, port number to receive ACKs from the receiver, timeout interval (milliseconds), and name of the file: ")
info = info.split(" ")
host_address = str(info[0]) # first input is host address
receive_port = int(info[1]) # second input is port for receiver to use
send_port = int(info[2]) # third input is port for sender to send data/receive acks
time_out = int(info[3]) # fourth input is timeout interval in milliseconds
file_name = str(info[4]) # fifth input is name of file w extension

# open file, read contents, store in data string
file = open(file_name, 'r')
data = file.read()
file.close()

# create udp socket, bind send port to it
sender_socket = socket(AF_INET, SOCK_DGRAM)
sender_socket.bind(("", send_port))

# send packets and receive acks from receiver
# write seqnum to log file seqnum.log
# write ack to log file ack.log
seqnum_file = open("seqnum.log", 'w')
ack_file = open("ack.log", 'w')
seqnum = 0 # start seqnum at 0
while len(data) > 0: # run loop for n/500^k > 0 times
    file_data = data[0:500]
    packet = "1" + " " + str(seqnum) + " " + str(len(file_data)) + " " + str(file_data)
    sender_socket.sendto(packet.encode(), (host_address, receive_port))
    seqnum_file.write(str(seqnum) + "\n") # write each seqnum sent to log
    receive_data, receiver_address = sender_socket.recvfrom(2048)
    receive_data = receive_data.decode().split(" ")
    ack = int(receive_data[0])
    new_seqnum = int(receive_data[1])
    ack_file.write(str(new_seqnum) + "\n") # record ack to ack.log
    if seqnum != new_seqnum:
        continue
    else:
        seqnum += 1
        try:
            data = data[500:]
        except:
            data = ""

packet = "2" + " " + str(seqnum) + " " + "0"
sender_socket.sendto(packet.encode(), (host_address, receive_port))
seqnum_file.write(str(seqnum) + "\n") # write each seqnum sent to log
receive_data, receiver_address = sender_socket.recvfrom(2048)
receive_data = receive_data.decode().split(" ")
ack = int(receive_data[0])
new_seqnum = int(receive_data[1])
ack_file.write(str(new_seqnum) + "\n")

if ack == 2:
    seqnum_file.close()
    ack_file.close()
    sender_socket.close()

# localhost 11000 12000 50 test.txt