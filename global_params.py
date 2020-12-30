"""

global params module - static data shared with all code

"""

from scapy.arch import get_if_addr

# port of the server in hackaton
SERVER_PORT = 2002

# udp broadcast port
DESTINATION_PORT = 13117

# general timout constant for the game in seconds
OFFER_TIME_OUT = 10
# general buffer size for server\client communications
MAX_SIZE_BUFFER = 40960
# cookie - identifier message to be part of the typing game
MAGIC_COOKIE = 0xfeedbeef
# offer message type in udp
UDP_MSG_TYPE = 0x2

# message format for the udp message packing
MESSAGE_FORMAT = 'Ibh'

# team name for the client side
TEAM_NAME = "YOGA_MASTERS\n"

# IP TYPES
EMPTY_IP = ""
LOCAL_IP = "127.0.0.1"
DEV_IP = "172.1.0.2"
TEST_IP = get_if_addr('eth2')  # will get test ip
# IP TYPES

# timeout for getting characters in server from client during game in seconds
TIMEOUT_FOR_GETTING_CHARACTERS = 0.25

# current ip in use
IP = DEV_IP
