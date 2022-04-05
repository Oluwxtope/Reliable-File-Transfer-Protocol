from socket import *

# constants
ack_type = 0 # ack packet
data_type = 1 # data packet
eot_type = 2 # end of transmission packet

# parse_data(filename) ->  opens filename, reads and returns content in data string
def parse_data(filename: str) -> str:
    file = open(filename, 'r')
    data = file.read()
    file.close()
    return data

# create_packet(type, seqnum, length, data) creates a packet using arguments and encodes it
def create_packet(type: int, seqnum: int, data: str = "") -> str:
    packet = str(type) + " " + str(seqnum) + " " + str(len(data)) + " " + str(data)
    return packet.encode()

# read_packet(packet) reads bytes object and returns list of ack, seqnum, length, and data
def read_packet(packet: bytes) -> list:
    packet = packet.decode().split(" ")
    ack = int(packet[0])
    seqnum = int(packet[1])
    length = int(packet[2])
    data = str(" ".join(packet[3:]))
    return [ack, seqnum, length, data]