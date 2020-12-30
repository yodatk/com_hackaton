import socket
from struct import unpack_from
from global_params import *
import threading

game_ended = False


def get_input_and_send_to_server(tcp_socket):
    global game_ended
    while not game_ended:
        user_input = input('')
        if not game_ended:
            tcp_socket.sendall(user_input.encode('utf-8'))


def main():
    global game_ended

    # Create socket for server
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    udp_socket.bind((IP, 13117))

    print("Do Ctrl+c to exit the program !!")

    # Let'udp_socket send data through UDP protocol
    while True:
        global game_ended
        game_ended = False
        # send_data = input("Type some text to send =>")
        # udp_socket.sendto(send_data.encode('utf-8'), (socket.gethostname(), 2))
        # print("\n\n 1. Client Sent : ", send_data, "\n\n")
        data, address = udp_socket.recvfrom(MAX_UDP_MSG_SIZE)
        try:
            magic_cookie, msg_type, port = unpack_from(MESSAGE_FORMAT, data)
            if magic_cookie == MAGIC_COOKIE and msg_type == UDP_MSG_TYPE:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp_socket.connect((IP, port))
                tcp_socket.sendall('YOGA MASTERS\n'.encode('utf-8'))
                start_game_msg = tcp_socket.recv(MAX_TCP_SIZE_BUFFER)
                print(start_game_msg.decode('utf-8'))

                input_thread = threading.Thread(target=get_input_and_send_to_server, args=(tcp_socket,))
                input_thread.start()
                game_ended_msg = tcp_socket.recv(MAX_TCP_SIZE_BUFFER)
                game_ended = True
                print(game_ended_msg.decode('utf-8'))
        except:
            pass

        # print("\n\n 2. Client received : ",, "\n\n")
        # close the socket
    udp_socket.close()


if __name__ == '__main__':
    main()
