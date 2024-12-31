from sockets import server, client
import threading

client = False
server = False
c_server_ip = ''
c_server_on = False

def Start_Server():
    global server
    server = True
    socket_thread = threading.Thread(target=server.start_server)
    socket_thread.daemon = True
    socket_thread.start()

def Start_Client(server_ip):
    global client
    client = True
    socket_thread = threading.Thread(target=client.start_client, args=(server_ip,))
    socket_thread.daemon = True
    socket_thread.start()