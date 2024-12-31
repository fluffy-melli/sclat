from sockets import server, client
import threading

client = False
server = False
c_server_ip = ''
c_server_on = False

def Start_Server():
    global server
    server = True
    threading.Thread(target=server.start_server, daemon=True).start()

def Start_Client(server_ip):
    global client
    client = True
    threading.Thread(target=client.start_client, args=(server_ip,), daemon=True).start()