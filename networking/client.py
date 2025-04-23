import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = False
        self.socket = None

    def connect(self):
        print("Connecting...")
        if self.connected:
            print("Already connected! Doing a reconnect...")
            self.disconnect()
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
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
        

    def disconnect(self):
        if self.socket or self.connected:
            try:
                if self.socket:
                    self.socket.close()
                    self.connected = False
                    print("Socket closed successfully")
                else:
                    self.connected = False
                    print("Already disconnected!")
            except OSError as e:
                print(f"OS error: {e}")
            except ValueError as e:
                print(f"Value error: {e}")
            except RuntimeError as e:
                print(f"Runtime error: {e}")
            except AttributeError as e:
                print(f"Attribute error: {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

    def request(self, message, delimiter = '\n', encoding = 'utf-8', response_chunk_size = 1024):
        print("Sending request...")
        if not self.connected:
            print("Was not connected to server, trying to connect...")
            self.connect()

        self.sendall_with_errorlog(message.encode(encoding))
        try:
            self.response = self.receive_response(delimiter, encoding, response_chunk_size)
        except Exception as e:
            print(f'Error when receiving response: {e}')
            self.response = None
        return self.response
    
    def sendall_with_errorlog(self, encodedMessage):
        try:
            self.socket.sendall(encodedMessage)
        except socket.error as e:
            print(f"Socket error: {e}")
        except BlockingIOError as e:
            print(f"Blocking I/O error: {e}")
        except OSError as e:
            print(f"OS error: {e}")
        except ConnectionResetError as e:
            print(f"Connection reset by peer: {e}")
        except ConnectionAbortedError as e:
            print(f"Connection aborted by local host: {e}")
        except TimeoutError as e:
            print(f"Timeout error: {e}")
        except BrokenPipeError as e:
            print(f"Broken pipe error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def receive_with_errorlog(self, chunk_size):
        print(f'Receiving datachunk of size {chunk_size}')
        try:
            data = self.socket.recv(chunk_size)
            if not data:
                print("No data received!")
                self.disconnect() # When no data is received, we assume the connection as been closed
                return [1, None]
            else:
                print("Chunk received successfully!")
                return [0, data]
        except socket.error as e:
            print(f"Socket error: {e}")
        except BlockingIOError as e:
            print(f"Blocking I/O error: {e}")
        except OSError as e:
            print(f"OS error: {e}")
        except ConnectionResetError as e:
            print(f"Connection reset by peer: {e}")
        except ConnectionAbortedError as e:
            print(f"Connection aborted by local host: {e}")
        except TimeoutError as e:
            print(f"Timeout error: {e}")
        except BrokenPipeError as e:
            print(f"Broken pipe error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def receive_response(self, delimiter = '\n', encoding = 'utf-8', chunk_size = 1024):
        self.response_received = ''

        # Receive in chunks until delimiter is reached
        while True:
            self.response_message = self.receive_with_errorlog(chunk_size)
            if self.response_message[0] == 0:
                self.response_chunk = self.response_message[1]
            else:
                raise Exception("Error when receiving response, empty response!")
            self.decoded_response_chunk = self.response_chunk.decode(encoding)
            self.response_received += self.decoded_response_chunk

            if delimiter in self.decoded_response_chunk:
                self.response_received = self.response_received.split(delimiter)[0] # Remove delimitter and potential stuff after it
                break

        return self.response_received

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return self.port