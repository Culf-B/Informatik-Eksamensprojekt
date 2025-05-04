import socket
import threading

try:
    from . import connectionBaseplate
    from . import sharedObject
except ImportError as e:
    print(f'ImportError! {e}. Trying another way of import...')
    import connectionBaseplate
    import sharedObject
    print('Importing finished successfully!')

class Server:
    def __init__(self, host, port, timeout = 10, listener_backlog = 5):
        '''
        Socket server with error handling
        Leave host blank for localhost 
        '''
        self.host = host
        if self.host == "":
            self.host = socket.gethostname()
        
        self.port = port
        self.timeout = timeout
        self.listener_backlog = listener_backlog

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(self.timeout)

        self.connectedClients = []
        self.threads = []
        self.stop_event = threading.Event()

        self.sharedObjectEventHandler = sharedObject.SharedObjectEventHandler()

    def listen(self):
        '''
        Blocking function that listens for incoming connections and creates threads for them
        '''
        self.socket.listen(self.listener_backlog)

        while True:
            try:
                print("Listening for a connection...")
                client_socket, addr = self.socket.accept()
                print('Got a connection from %s' % str(addr))
            except TimeoutError as e:
                print(f'Listener timed out, expected every {self.timeout} seconds')
                continue

            client_connection_object = ClientHandler(client_socket, addr, self.stop_event, timeout = self.timeout)

            client_handler = threading.Thread(target = client_connection_object.doClientConnection)
            client_handler.start()
            
            self.threads.append(client_handler)
            self.connectedClients.append(client_connection_object)

    def stop(self):
        self.stop_event.set()
        print(f'Stopping all connections. Waiting for timeout, max {self.timeout} seconds...')

        for i, t in enumerate(self.threads):
            if t.is_alive():
                print(f'Waiting for thread {i} to finish...')
                t.join()
    
        self.socket.close()
        print("All threads and server closed successfully!")

class ClientHandler(connectionBaseplate.Connection):
    def __init__(self, socket, address, stop_event, timeout = 10):
        self.socket = socket
        self.address = address
        self.stop_event = stop_event

        super().__init__(socket, timeout = timeout)
    
    def doClientConnection(self):
        '''
        Blocking function that keeps conversation with the client (request -> response)
        '''
        while True:
            if self.stop_event.is_set():
                print("Thread stopping because of stop event.")
                self.disconnect()
                return
            else:
                if self.connected:
                    try:
                        self.request_received = self.receive_request()
                        if self.request_received != None:
                            print(self.request_received)
                            self.serverToClientComms("ok!")
                    except Exception as e:
                        print(f'Disconnecting! Reason: {e}')
                        self.disconnect()
                else:
                    print("Unable to do client connection, not connected!")
                    return

    def serverToClientComms(self, message, delimiter = '\\n', encoding = 'utf-8'):
        print("Sending message...")
        if not self.connected:
            print("Not connected to any client!")
            return

        self.messageToSend = str(message) + str(delimiter)
        self.sendall_with_errorlog(self.messageToSend.encode(encoding))
        print("Message has been sent!")

    def receive_request(self, delimiter = '\\n', encoding = 'utf-8', chunk_size = 1024):
        self.response_received = ''

        # Receive in chunks until delimiter is reached
        while True:
            self.response_message = self.receive_with_errorlog(chunk_size)
            if self.response_message != None:
                if self.response_message[0] == 0:
                    self.response_chunk = self.response_message[1]
                else:
                    print("Empty response chunk! Message abandoned!")
                    self.response_received = None
                    return self.response_received
            else:
                raise Exception("Error when receiving response chunk!")
            self.decoded_response_chunk = self.response_chunk.decode(encoding)
            self.response_received += self.decoded_response_chunk

            if delimiter in self.response_received:
                self.response_received = self.response_received.split(delimiter)[0] # Remove delimitter and potential stuff after it
                print("Delimiter in response!")
                break

        return self.response_received

if __name__ == '__main__':

    addr = ""
    port = 5000
    print(f'Starting server on addr: {addr}, port: {port}')
    server = Server("", 5000)
    try:
        server.listen()
    except KeyboardInterrupt:
        print("KeyboardInterupt! Initiating shutdown...")
        server.stop()
        print("Shutdown complete!")