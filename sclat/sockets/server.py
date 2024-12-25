from sockets import setting, user
import threading, socket, json

playurl = ''
seek = 0
clients = []

def handle_client(client_socket, client_address, clients):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            try:
                message_data = json.loads(data.decode('utf-8'))
                message_type = message_data.get('type')
                if message_type == "req-play-info":
                    if playurl != '':
                        response = {"type": "play-info", "playurl": playurl, "seek": seek}
                    else:
                        response = {"type": "play-wait"}
                    client_socket.send(json.dumps(response).encode('utf-8'))
            except json.JSONDecodeError:
                pass

    except Exception as e:
        pass
    finally:
        if client_socket in clients:
            clients.remove(client_socket)
        client_socket.close()

def broadcast_message(message):
    for client in clients[:]:
        try:
            data = json.dumps(message)
            client.send(data.encode('utf-8'))
        except Exception as e:
            print(f"클라이언트에게 메시지 전송 중 오류 발생: {e}")
            if client in clients:
                clients.remove(client)

def start_server():
    global clients
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 12377))
    server.listen(setting.max_client)
    print(f"SERVER START (ADDRESS) : {user.get_internal_ip()} / {user.get_external_ip()} [NEED PORT FORWARDING -> :12377]")

    while True:
        client_socket, client_address = server.accept()
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address, clients))
        client_thread.start()
