from pypresence import Presence
from setting import setting as user_setting
import time

RPC = Presence(1308354144490360943)
def update(start_time, name="Picking a Video", url="", channel="Still choosing..."):
    update_params = {
        "details": f"{name}",
        "state": f"{channel}",
        "start": start_time,
        "large_image": "./asset/sclatLogo.png",
        "large_text": "https://github.com/fluffy-melli/sclat",
        "buttons": [
            {
                "label": "Watch Video",
                "url": url
            }
        ]
    }
    
    if not url:
        update_params.pop("buttons")
        
    RPC.update(**update_params)

def default():
    if user_setting.discord_RPC:
        update(time.time())