import socket

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
        socket.settimout(self.timeout)

    def listen(self):
        '''
        Blocking function that listens for incoming connections and creates threads for them
        '''
        self.socket.listen(self.listener_backlog)

        while True:
            client_socket, addr = self.socket.accept()  # establish a connection with client
            print('Got a connection from %s' % str(addr))
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

class ClientHandler:
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
    
    def doClientConnection(self):
        '''
        Blocking function that keeps conversation with the client (request -> response)
        '''
        while True:
            data = client_socket.recv(64).decode('utf-8')
            if not data:
                break
            print('Received from client: ' + data)
            message = input(" -> ")  # take input from server
            client_socket.send(message.encode('utf-8'))  # send message
        client_socket.close()