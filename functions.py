from socket import *

# packet types
# ack packet: ack = 0, seqnum = seqnuence num of packet being acked, len = 0, data = ""
ack_type = 0
# data packet: data = 1, seqnum = seqnuence num of packet, len = length of data, data = str data
data_type = 1
# eot packet: eot = 2, seqnum = -1, len = 0, data = ""
eot_type = 2

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