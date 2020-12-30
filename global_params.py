"""

global params module - static data shared with all code

"""

from scapy.arch import get_if_addr

SERVER_PORT = 2002
DESTINATION_PORT = 13117
OFFER_TIME_OUT = 10

MAX_SIZE_BUFFER = 40960

MAGIC_COOKIE = 0xfeedbeef
UDP_MSG_TYPE = 0x2

MESSAGE_FORMAT = 'Ibh'

TEAM_NAME = "team_name\n"
EMPTY_IP = ""
LOCAL_IP = "127.0.0.1"
DEV_IP = "172.1.0.2"
TEST_IP = get_if_addr('eth2') # will get test ip

#current ip in use 
IP = DEV_IP
