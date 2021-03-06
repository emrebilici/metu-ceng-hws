import hashlib
import sys

# this flag is set to True to make tests on our local machine, see below if / else blocks
ON_LOCAL = False

# debug prints are enabled / disabled
DEBUG = False

# window size for our Go-Back-N implementation
RDT_WINDOW_SIZE = 16

# timeout value in seconds for receiver threads waiting for ACK packets
TIMEOUT = 2.5 * RDT_WINDOW_SIZE * 1e-3

# file size in bytes
TOTAL_BYTES = 5 * 1000 * 1000

CHECKSUM_SIZE = 32
SEQUENCE_NUM_SIZE = 6
PAYLOAD_SIZE = 500

# > packet format

# Packet Format:
# < PAYLOAD | SEQUENCE | CHECKSUM >
# CHECKSUM is computed over < PAYLOAD | SEQUENCE >
# Then concatenated

DATA_HEADER_SIZE = CHECKSUM_SIZE + SEQUENCE_NUM_SIZE

DATA_PACKET_SIZE = PAYLOAD_SIZE + DATA_HEADER_SIZE

# packet format <

NUMBER_OF_PACKETS = TOTAL_BYTES // PAYLOAD_SIZE

ACK_PACKET_SIZE = SEQUENCE_NUM_SIZE + CHECKSUM_SIZE

# Interfaces
if ON_LOCAL:
    INTERFACE_1 = "localhost"
    INTERFACE_2 = "localhost"
    INTERFACE_3 = "localhost"
    INTERFACE_4 = "localhost"
    INTERFACE_5 = "localhost"
    INTERFACE_6 = "localhost"
    INTERFACE_7 = "localhost"
    INTERFACE_8 = "localhost"
    INTERFACE_9 = "localhost"

    PORT_1 = 8101
    PORT_2 = 8102
    PORT_3 = 8103
    PORT_4 = 8104
    PORT_5 = 8105
    PORT_6 = 8106
    PORT_7 = 8107
    PORT_8 = 8108
    PORT_9 = 8109

else:
    INTERFACE_1 = "10.10.1.2"
    INTERFACE_2 = "10.10.2.1"
    INTERFACE_3 = "10.10.2.2"
    INTERFACE_4 = "10.10.3.1"
    INTERFACE_5 = "10.10.3.2"
    INTERFACE_6 = "10.10.4.1"
    INTERFACE_7 = "10.10.4.2"
    INTERFACE_8 = "10.10.5.1"
    INTERFACE_9 = "10.10.5.2"

    __COMMON_PORT = 8100

    # We use the same port throughout the network for simplicity
    PORT_1 = __COMMON_PORT
    PORT_2 = __COMMON_PORT
    PORT_3 = __COMMON_PORT
    PORT_4 = __COMMON_PORT
    PORT_5 = __COMMON_PORT
    PORT_6 = __COMMON_PORT
    PORT_7 = __COMMON_PORT
    PORT_8 = __COMMON_PORT
    PORT_9 = __COMMON_PORT

# our encoding standard for bytearrays within the project
ENCODING = "utf-8"


# converts bytearray to int
def get_int_from_binary(byte):
    return int(byte.decode(ENCODING))


# calculate checksum and return as bytearray
def checksum(payload_sequence):
    md5 = hashlib.md5()

    md5.update(payload_sequence)

    return bytearray(md5.hexdigest(), ENCODING)


def debug(msg):
    if DEBUG:
        print(msg, file=sys.stderr)


def get_ack_sequence_number(ack_packet):
    return int(ack_packet[:SEQUENCE_NUM_SIZE])


def get_sequence_number(packet):
    return int(packet[PAYLOAD_SIZE: PAYLOAD_SIZE + SEQUENCE_NUM_SIZE])


ZERO = ord(str(0))
NINE = ord(str(9))


def is_corrupted(packet):
    intermediate = packet[:PAYLOAD_SIZE + SEQUENCE_NUM_SIZE]
    packet_sequence_number = intermediate[PAYLOAD_SIZE:]
    packet_checksum = packet[PAYLOAD_SIZE + SEQUENCE_NUM_SIZE:]

    # if sequence number part contains non numeric characters, then packet is corrupted
    corrupted = any(map(lambda b: b < ZERO or b > NINE, packet_sequence_number))

    if not corrupted:
        # if computed checksum is not equal to extracted checksum, then packet is corrupted
        corrupted = checksum(intermediate) != packet_checksum

    return corrupted


def is_ack_corrupted(packet):
    packet_sequence_number = packet[:SEQUENCE_NUM_SIZE]
    packet_checksum = packet[SEQUENCE_NUM_SIZE:]

    # if sequence number part contains non numeric characters, then packet is corrupted
    corrupted = any(map(lambda b: b < ZERO or b > NINE, packet_sequence_number))

    if not corrupted:
        # if computed checksum is not equal to extracted checksum, then packet is corrupted
        corrupted = checksum(packet_sequence_number) != packet_checksum

    return corrupted
