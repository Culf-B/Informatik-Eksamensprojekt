import socket

class Connection:
    def __init__(self, socket, connected = True, timeout = 10):
        '''
        Socket connection baseplate object with error handling
        Leave host blank for localhost
        '''
        self.socket = socket
        self.timeout = timeout
        self.connected = connected
        
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
                print(f'Chunk received successfully! Chunk: {data}')
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