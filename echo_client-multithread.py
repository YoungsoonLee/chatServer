import sys
import socket
import threading
import tincanchat

HOST = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
PORT = tincanchat.PORT


def handle_input(sock):
    """ Prompt user for message and send it to server """
    print("Type messages, enter to send. 'q' to quit")
    while True:
        msg = input()  # blocks
        if msg == 'q':
            # sock.shutdown(socket.SHUT_RDWR)
            sock.close()
            break
        try:
            tincanchat.send_msg(sock, msg)  # blocks until sent
        except (BrokenPipeError, ConnectionError):
            break


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print('Connected to {}:{}'.format(HOST, PORT))

    # Create thread for handling user input and message sending
    thread = threading.Thread(target=handle_input, args=[sock], daemon=True)
    thread.start()
    rest = bytes()
    addr = sock.getsockname()
    # Loop indefinitely to receive messages from server
    while True:
        try:
            print(type(sock))
            # blocks
            (msgs, rest) = tincanchat.recv_msgs(sock, rest)
            for msg in msgs:
                print(msg)
        except ConnectionError:
            print('Connection to server closed')
            sock.close()
            break
