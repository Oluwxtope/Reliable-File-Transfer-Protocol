from socket import *
from random import *

# request input from user
info = input("Enter the UDP port number to receive packet, drop probability, and name of the file received packet will be written: ")
info = info.split(" ")
receive_port = int(info[0]) # first input is port to receive packet
drop_probability = float(info[1]) # second input is probability of packet being dropped
file_name = str(info[2]) # third input is name of file to write
file = open(file_name, 'w')

# create udp socket, bind it to receive port
receiver_socket = socket(AF_INET, SOCK_DGRAM)
receiver_socket.bind(("", receive_port))

# receive packets and write to log file arrival.log
# drop packets based on drop probability and write to log file drop.log
# write acked packets to new file
arrival = open("arrival.log", 'w')
dropped = open("drop.log", 'w')
last_seqnum = -1
while True:
    packet, sender_address = receiver_socket.recvfrom(2048)
    packet = packet.decode().split(" ")
    ack = int(packet[0])
    seqnum = int(packet[1])
    length = int(packet[2])
    arrival.write(str(seqnum) + "\n") # record seqnum to arrival.log
    if ack == 1:
        text = str(" ".join(packet[3:]))
        if False: #random() < drop_probability / 100:
            #dropped.write(str(seqnum) + "\n")
            continue
        elif seqnum == last_seqnum:
            continue
        elif seqnum - 1 == last_seqnum:
            file.write(text)
            packet = "0" + " " + str(seqnum) + " " + "0"
            receiver_socket.sendto(packet.encode(), sender_address)
            last_seqnum = seqnum
            continue
    elif ack == 2:
        packet = "2" + " " + str(seqnum) + " " + "0"
        receiver_socket.sendto(packet.encode(), sender_address)
        break

arrival.close()
dropped.close()
file.close()
receiver_socket.close()

# 11000 0.5 new.txt