import pygame

load = 0 # 0 = choice / 1 = download / 2 = play
win, font, vid = None, None, None

def reset(size, vid=None):
    global win, font
    pygame.init()
    pygame.mixer.init(frequency=22050, size=-16, channels=2)
    if vid is None:
        win = pygame.display.set_mode(size, pygame.RESIZABLE)
    else:
        win = pygame.display.set_mode(size)
    try:
        font = pygame.font.Font("./asset/NanumBarunpenB.ttf", 20)
    except FileNotFoundError:
        font = pygame.font.Font(None, 20)