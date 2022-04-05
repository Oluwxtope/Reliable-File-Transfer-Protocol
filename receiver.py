from functions import *
from socket import *
from random import *
from time import *

def main():
    # request input from user
    info = input("Enter the UDP port number to receive packet, drop probability, and name of the received file: ")
    info = info.split(" ")
    receive_port = int(info[0]) # first input is port to receive packet
    drop_probability = float(info[1]) # second input is probability of packet being dropped
    file_name = str(info[2]) # third input is name of file to write

    # create udp socket, bind it to receive port
    receiver_socket = socket(AF_INET, SOCK_DGRAM)
    receiver_socket.bind(("", receive_port))

    # open log files arrival.log and drop.log
    arrival = open("arrival.log", 'w')
    dropped = open("drop.log", 'w')
    received = {} # packets received  in order go to received dict
    transmission = None
    while True:
        packet, sender_address = receiver_socket.recvfrom(2048)
        ack, seqnum, length, data = read_packet(packet)
        arrival.write(str(seqnum) + "\n") # record seqnum to arrival.log
        if ack == data_type:
            transmission = data_type
            if random() < drop_probability: # drop packets based on drop probability and write to log file drop.log
                dropped.write(str(seqnum) + "\n")
            else:
                if seqnum in received: # if packet already received and in order move on
                    continue
                else:
                    received[seqnum] = data
        elif ack == eot_type: # if packet received is eot, send an eot to sender and close the socket
            if transmission == data_type:
                transmission = eot_type
                for seqnum in received:
                    ack_packet = create_packet(ack_type, seqnum)
                    receiver_socket.sendto(ack_packet, sender_address)
                packet = create_packet(eot_type, -1)
                receiver_socket.sendto(packet, sender_address)
                continue
            else:
                transmission = eot_type
                packet = create_packet(eot_type, -1)
                receiver_socket.sendto(packet, sender_address)
                receiver_socket.close()
                break

    dropped.close()
    arrival.close()

    # write the received packets in order
    file = open(file_name, 'w')
    for seqnum in range(0, len(received)):
        file.write(received[seqnum])
    file.close()

main()