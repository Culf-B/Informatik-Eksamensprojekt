import socket
import json
import threading
from time import sleep

from . import connectionBaseplate

class Client(connectionBaseplate.Connection):
    def __init__(self, host, port, updateCallback, timeout = 10):
        '''
        Client with some error handling
        Leave host blank for localhost
        '''
        self.host = host
        if self.host == "":
            self.host = socket.gethostname()
        self.port = port
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout = timeout
        self.socket.settimeout(self.timeout)

        self.updateCallback = updateCallback

        self.updateListener = threading.Thread(target = self.listen_for_updates, daemon = True)
        self.updateListener.start()

        super().__init__(self.socket, connected = self.connected, timeout = self.timeout)

    def connect(self):
        print("Connecting...")
        if self.connected:
            print("Already connected! Doing a reconnect...")
            self.disconnect()
        try:
            self.socket.connect((self.host, self.port))
            self.socket.settimeout(self.timeout)
            self.connected = True
            print("Connected successfully")
        except socket.error as e:
            print(f"Socket error: {e}")
        except OSError as e:
            print(f"OS error: {e}")
        except ConnectionRefusedError as e:
            print(f"Connection refused by the remote host: {e}")
        except ConnectionResetError as e:
            print(f"Connection reset by the peer: {e}")
        except TimeoutError as e:
            print(f"Timeout error: {e}")
        except socket.gaierror as e:
            print(f"Address-related error: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def request(self, message, delimiter = '\\n', encoding = 'utf-8'):
        print("Sending request...")
        if not self.connected:
            print("Was not connected to server, trying to connect...")
            self.connect()

        self.messageToSend = str(message) + str(delimiter)

        self.sendall_with_errorlog(self.messageToSend.encode(encoding))

    def receive_response(self, delimiter = '\\n', encoding = 'utf-8', chunk_size = 1024):
        self.response_received = ''

        # Receive in chunks until delimiter is reached
        while True:
            self.response_message = self.receive_with_errorlog(chunk_size)
            if self.response_message != None:
                if self.response_message[0] == 0:
                    self.response_chunk = self.response_message[1]
                else:
                    raise Exception("Empty response chunk!")
            else:
                raise Exception("Error when receiving response chunk!")
            self.decoded_response_chunk = self.response_chunk.decode(encoding)
            self.response_received += self.decoded_response_chunk

            if delimiter in self.response_received:
                self.response_received = self.response_received.split(delimiter)[0] # Remove delimitter and potential stuff after it
                print("Delimiter in response!")
                break

        return self.response_received
    
    def listen_for_updates(self):
        while True:
            if self.isConnected():
                try:
                    response = self.receive_response()
                    self.updateCallback(response)
                except Exception as e:
                    print(f'Error when listening for updates: {e}')
            else:
                print("Can't listen for updates, not connected! Retrying in 5 seconds...")
                sleep(5)

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port
    
    def isConnected(self):
        return self.connected

if __name__ == '__main__':
    client = Client("", 5000)
    client.connect()
    if client.isConnected():
        print(client.request(input(" -> ")))
    client.disconnect()