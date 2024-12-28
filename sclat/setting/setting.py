from setting import json

json_file_path = "./setting/setting.json"
def init_file():
    data = {}
    data['discord_RPC'] = True
    data['Gesture-Control'] = False
    data['Gesture-Control-Screen'] = False
    # data['STT-Contorl'] = False
    data['volume'] = 10
    data['file-save-dir'] = './asset/storage'
    data['Subtitle-Lang'] = 'ko'
    return data
def change_setting_data(key:str,value):
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
    data[key] = value
    json.write(json_file_path,data)
    reload_setting_file()
def reload_setting_file():
    global discord_RPC,Gesture,Gesture_show,stt,SubTitle,volume,file_save_dir
    data = json.read(json_file_path)
    if data == None:
        data = init_file()
        json.write(json_file_path,data)
    discord_RPC = data['discord_RPC']
    Gesture = data['Gesture-Control']
    Gesture_show = data['Gesture-Control-Screen']
    # stt = data['STT-Contorl']
    volume = data['volume']
    file_save_dir = data['file-save-dir']
    SubTitle = data['Subtitle-Lang']
#####################
discord_RPC = None
Gesture = None
Gesture_show = None
# stt = None
volume = None
file_save_dir = None
SubTitle = 'ko'
reload_setting_file()