from gui.addon import with_play
import socket, json, time

client = None
play = False
url = ''
seek = 0

def playinfo():
    try:
        data = json.dumps({"type": "req-play-info"})
        client.send(data.encode('utf-8'))
    except Exception as e:
        return None

def start_client(server_ip):
    global client, play, url, seek
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, 12377))
        with_play.c_server_on = True
    except socket.gaierror as e:
        print(f"Error resolving IP: {e}")
        with_play.c_server_ip = ''
        with_play.c_server_on = False
        return
    except ConnectionRefusedError as e:
        print(f"Connection failed: {e}")
        with_play.c_server_ip = ''
        with_play.c_server_on = False
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        with_play.c_server_ip = ''
        with_play.c_server_on = False
        return
    try:
        playinfo()
        while True:
            time.sleep(2)
            response = client.recv(1024)
            try:
                message_data = json.loads(response.decode('utf-8').split("}{")[0] + "}")
            except Exception as e:
                message_data = json.loads(response.decode('utf-8'))
            type = message_data.get('type')
            print(message_data)
            if type == "play-info":
                play = True
                url = message_data.get('playurl')
                seek = message_data.get('seek')
            if type == "play-wait":
                play = False
    except KeyboardInterrupt:
        pass
    finally:
        client.close()
