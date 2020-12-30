'''

server module - accept connections from team 
for a keyboard game and calculate results

'''
import socket
import threading
from concurrent.futures.thread import ThreadPoolExecutor
import time
import GameLogicSingleton
from global_params import *
from struct import pack
import random
from scapy.arch import get_if_addr
from unbuffered import Unbuffered
import sys
# printing to sys.out without buffer
sys.stdout = Unbuffered(sys.stdout)



def parse_join_tcp_msg(data: str):
    """
    
    :return: data

    """
    if data.strip() == '':
        return None
    else:
        return data


def parse_join_team_name_msg(data: str):
    if data.strip() == '':
        return None
    else:
        return data[:data.find('\n')]


def receive_tcp_offers():
    # Create TCP socket
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_socket.bind((EMPTY_IP, SERVER_PORT))
    tcp_socket.listen(1)
    print("server now listening")
    while True:
        connection, client_address = tcp_socket.accept()  # .recvfrom(MAX_UDP_MSG_SIZE)
        if not GameLogicSingleton.get_instance().game_running:
            data = connection.recv(MAX_SIZE_BUFFER)
            print("got new tcp connection")
            team_name = parse_join_team_name_msg(data.decode('utf-8'))
            print(f"team: {team_name} establish connection")
            if team_name is not None:
                GameLogicSingleton.get_instance().assign_team_to_group(team_name, connection)


def pack_offer_message():
    return pack(MESSAGE_FORMAT, MAGIC_COOKIE, UDP_MSG_TYPE, SERVER_PORT)


def send_msg_to_players(to_send_connection, msg):
    print("sending message to some player")
    to_send_connection.sendall(msg.encode('utf-8'))
    print("finished sending message to some player")


def listen_and_count_team(team_name, connection):
    while True:
        try:
            data = connection.recv(MAX_SIZE_BUFFER)
            if data is not None and len(data) > 0 and GameLogicSingleton.get_instance().game_running:
                chars_after_decode = parse_join_tcp_msg(data.decode('utf-8')) 
                if chars_after_decode is not None:
                    score = len(chars_after_decode)
                    GameLogicSingleton.get_instance().add_score_to_group(team_name, score_to_add=score)
        except Exception as e:
            #print(e)
            pass
        finally:
            time.sleep(0.25)


if __name__ == '__main__':
    
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    # Bind the socket to the port
    server_address = (EMPTY_IP, SERVER_PORT)
    
    udp_socket.bind(server_address)
    start_msg = f"Server started, listening on IP address {IP}"
    print(start_msg)

    accepting_thread = threading.Thread(target=receive_tcp_offers)
    accepting_thread.start()

    while True:
        try:
        # main thread - sending udp broadcast offers every 1 second for 10 seconds
            timeout = time.time() + OFFER_TIME_OUT
            while time.time() < timeout:
                udp_socket.sendto(pack_offer_message(), ('<broadcast>', DESTINATION_PORT))
                time.sleep(1)
            # game is now running, cannot accept more teams
            GameLogicSingleton.get_instance().game_running = True
            print("Game is starting - no more connections")
            groups = {**GameLogicSingleton.get_instance().group1, **GameLogicSingleton.get_instance().group2}
            if len(groups) >= 1:
                keys = list(groups.keys())
                random.shuffle(keys)
                thread_pool_executor = ThreadPoolExecutor(max_workers=len(keys))
                for team_name in keys:
                    thread_pool_executor.submit(send_msg_to_players, groups[team_name],
                                                GameLogicSingleton.get_instance().generate_welcome_msg())
                thread_pool_executor.shutdown(wait=True)
                print("finished sending opening message for players")
                thread_pool_executor = ThreadPoolExecutor(max_workers=len(keys))
                random.shuffle(keys)
                print("start listening for teams chars:")
                for team_name in keys:
                    print(team_name)
                    team_connection = groups[team_name]
                    thread_pool_executor.submit(listen_and_count_team, team_name, team_connection)

                
                # main thread -> wait for game to finish
                time.sleep(10)

                print("time is out!! need to calculate scores")
                thread_pool_executor.shutdown(wait=False)
                print("no more accepting chars")
                random.shuffle(keys)
                thread_pool_executor = ThreadPoolExecutor(max_workers=len(keys))
                for team_name in keys:
                    thread_pool_executor.submit(send_msg_to_players, groups[team_name],
                                                GameLogicSingleton.get_instance().generate_end_msg())

                thread_pool_executor.shutdown(wait=True)
            
        except Exception as e:
            print(e)
        finally:
            print("game is finished - restarting")
            GameLogicSingleton.get_instance().reset()
            
            



