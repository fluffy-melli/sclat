import sys,time
from src import gui, nogui
import src.win.screen
from src.utils import user_setting
import src.discord.client
import src.with_play
import locale, threading
from pypresence.exceptions import DiscordNotFound

args = sys.argv[1:]

nogui_op = False
once_op = False
playlist_op = False

for arg in args:
    if not arg.startswith("--") and playlist_op:
        src.win.setting.video_list.append(arg)
    elif arg.startswith("--") and arg != "--play":
        playlist_op = False
    if arg == "--nogui":
        nogui_op = True
    if arg == "--once":
        once_op = True
    if arg == "--play":
        playlist_op = True
    if arg == "--with-play-server":
        src.with_play.Start_Server()
    if arg == "--with-play-client":
        src.with_play.client = True

try:
    if user_setting.discord_RPC:
        src.discord.client.RPC.connect()
        src.discord.client.update(time.time(),"waiting...")

    while True:
        src.win.screen.load = 0
        if nogui_op:
            nogui.wait(once_op)
            break
        else:
            gui.wait(once_op)
            break

except DiscordNotFound:
    system_lang = locale.getdefaultlocale()[0]
    if system_lang and system_lang.startswith('ko'):
        error_msg = "Discord가 실행되어 있지 않습니다.\nDiscord를 실행한 후 다시 시도하거나,\nsetting.json 파일에서 discord_RPC 값을 false로 변경해주세요."
    else:
        error_msg = "Discord is not running.\nPlease start Discord and try again,\nor set discord_RPC to false in setting.json file."
    print(error_msg)
    sys.exit(1)

if user_setting.discord_RPC:
    src.discord.client.RPC.close()