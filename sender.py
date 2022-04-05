from functions import *
from socket import *
from time import *

def main():
    # request input from user
    info = input("Enter the host address of the receiver, port number to used to send data, port number to receive ACKs from the receiver, timeout interval (milliseconds), and name of the file to send: ")
    info = info.split(" ")
    host_address = str(info[0]) # first input is host address
    receive_port = int(info[1]) # second input is port for receiver to use
    send_port = int(info[2]) # third input is port for sender to send data/receive acks
    countdown = float(info[3]) # fourth input is timeout interval in milliseconds
    file_name = str(info[4]) # fifth input is name of file w extension

    # get file contents and arrange into packets in dictionary
    data = parse_data(file_name)
    packets = {} # store packets to send
    acked_packet = {} # record packet seqnum and whether acked or not
    packet_seqnum = 0
    while len(data) > 0: # run loop for n/500^k > 0 times
        packets[packet_seqnum] = data[0:500] # packet is first 500 chars in data
        acked_packet[packet_seqnum] = False # packet not acked
        data = data[500:] # move on to remaining chars in data
        packet_seqnum += 1

    # create udp socket, bind send port to it
    sender_socket = socket(AF_INET, SOCK_DGRAM)
    sender_socket.bind(("", send_port))
    sender_socket.setblocking(False) # make sure sender_socket isn't in blocking mode...

    # open log files seqnum.log and ack.log
    seqnum_file = open("seqnum.log", 'w')
    ack_file = open("ack.log", 'w')

    # send packets to receiver, record in seqnum.log, receive acks, record in ack.log
    all_acked = False # all packets acked by receiver?
    while not all_acked:
        for seqnum in packets: # send each packet in packets dict to receiver, record in seqnum.log
            if not acked_packet[seqnum]:
                packet = create_packet(data_type, seqnum, packets[seqnum])
                sender_socket.sendto(packet, (host_address, receive_port))
                seqnum_file.write(str(seqnum) + "\n") # write each seqnum sent to log
        packet = create_packet(eot_type, -1)
        sender_socket.sendto(packet, (host_address, receive_port))
        seqnum_file.write(str(list(packets.keys())[-1] + 1) + "\n") # write each seqnum sent to log
        
        deadline = time() + countdown/1000 # set deadline to be countdown ms/1000 ms/s
        while time() < deadline: # run loop looking for ack packets until countdown is over and deadline met...
            try: 
                received_packet, receiver_address = sender_socket.recvfrom(2048)
                received_ack, received_seqnum, received_length, received_data = read_packet(received_packet)
                ack_file.write(str(received_seqnum) + "\n")
                if received_ack == ack_type and not acked_packet[received_seqnum]: # if packet is ack packet and packet hasn't previously been acked by received
                    acked_packet[received_seqnum] = True
                else:
                    break
            except: # loop will run continuously until deadline met if socket has no data
                continue

        all_acked = True # assume all packets acked, run loop to verify
        for seqnum in acked_packet:
            if not acked_packet[seqnum]:
                all_acked = False
                break # if packet not acked, break loop...
        
        if all_acked: # if all packets acked, send eot packet and close all files... 
            sender_socket.setblocking(True)
            packet = create_packet(eot_type, -1)
            sender_socket.sendto(packet, (host_address, receive_port))
            seqnum_file.write(str(list(packets.keys())[-1] + 1) + "\n") # write each seqnum sent to log
            received_packet, receiver_address = sender_socket.recvfrom(2048)
            received_ack, received_seqnum, received_length, received_data = read_packet(received_packet)
            ack_file.write(str(received_seqnum) + "\n")
            if received_ack == 2:
                seqnum_file.close()
                ack_file.close()
                sender_socket.close()
                break

main()