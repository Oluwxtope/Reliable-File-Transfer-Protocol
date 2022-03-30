from socket import *

# handle program startup, request inputs from user
info = input("Enter the host address of the receiver, UDP port number to send data to the receiver, UDP port number to receive ACKs from the receiver, timeout interval (milliseconds), and name of the file: ")
info = info.split(" ")
host_address = str(info[0])
send_port = int(info[1])
receive_port = int(info[2])
time_out = int(info[3])
file_name = str(info[4])

# open file, read contents, store in data
file = open(file_name, 'r')
data = file.read()
file.close()

# create udp socket
receiver_socket = socket(AF_INET, SOCK_DGRAM)
receiver_socket.bind(("", receive_port))

# send packets
seqnum = 0
seqnum_file = open("seqnum.log", 'w')
while len(data) > 0:
    packet_data = data[0:500]
    try:
        data = data[500:]
    except:
        data = ""
    packet = "1" + " " + str(seqnum) + " " + str(len(packet_data)) + str(packet_data)
    receiver_socket.sendto(packet.encode(), (host_address, receive_port))
    seqnum_file.write(str(seqnum))
    seqnum += 1

# receive acks
ack_file = open("ack.log", 'w')

