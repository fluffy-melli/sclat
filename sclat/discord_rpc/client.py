from pypresence import Presence

RPC = Presence(1308354144490360943)
def update(start_time,name,url,channel):
    RPC.update(
        details=f"{name}",
        state=f"{channel}",
        start=start_time,
        large_image="sclatlogo",
        large_text="https://github.com/fluffy-melli/sclat",
        buttons=[
            {
                "label": "Watch Video",
                "url": url
            }
        ]
    )