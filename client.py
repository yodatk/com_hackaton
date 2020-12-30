"""
client module - reaced to broadcasts
and participate in the keyboard game..
single threaded - can only play one game at a time
"""

import socket
import struct
from struct import unpack_from
from global_params import *
import threading
import time

# global param to know if the current game ended
game_ended = False


def get_input_and_send_to_server(tcp_socket):
    """

    :param tcp_socket: tcp socket to write the chars into it
    :return: none
    """
    global game_ended

    while not game_ended:
        try:
            user_input = input('')
            if not game_ended:
                tcp_socket.sendall(user_input.encode('utf-8'))
        except:
            # catch any exception that can occur from ilegal keys that entered by user
            pass


def main():
    """
    main function runs in a loop and react to broadcasts,
    first sending the team name and then wait for the welcoming message from the server
    and start hitting the keyboard
    :return:
    """
    global game_ended

    # Create socket for server
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.bind((EMPTY_IP, DESTINATION_PORT))

    print("Do Ctrl+c to exit the program !!")

    # Let'udp_socket send data through UDP protocol
    while True:
        global game_ended
        game_ended = False
        # listening from broadcasts from any server
        data, address = udp_socket.recvfrom(MAX_SIZE_BUFFER)
        try:
            # get udp message and process it according to pre defined format
            magic_cookie, msg_type, port = unpack_from(MESSAGE_FORMAT, data)

            # check data is matching the expected one - magic cookie and msg type
            if magic_cookie == MAGIC_COOKIE and msg_type == UDP_MSG_TYPE:
                # msg verfied - now we try to establish connection with the server
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.connect((address[0], port))

                # TCP connection established with server - sending Team Name
                tcp_socket.sendall(TEAM_NAME.encode('utf-8'))

                # Waiting for Start Game Message from Server
                start_game_msg = tcp_socket.recv(MAX_SIZE_BUFFER)
                print(start_game_msg.decode('utf-8'))

                # Game Started - make single thread to push keyboard keys - and send them over tcp
                input_thread = threading.Thread(target=get_input_and_send_to_server, args=(tcp_socket,))
                input_thread.start()

                # meanwhile wait for another msg from server - the end game msg
                game_ended_msg = tcp_socket.recv(MAX_SIZE_BUFFER)
                game_ended = True
                print(game_ended_msg.decode('utf-8'))

                # close all connection
                tcp_socket.shutdown(socket.SHUT_RDWR)
                tcp_socket.close()
                print("Server disconnected, listening for offer requests...")

        except struct.error as e:
            # server with address info: ({address[0]},{address[1]}) didn't send corrent data"
            pass

        except ConnectionRefusedError as e:
            # catch connection refused error
            pass
        except:
            # catch any other unexpected error to keep client alive and flow
            pass
        finally:

            time.sleep(1)


if __name__ == '__main__':
    main()
