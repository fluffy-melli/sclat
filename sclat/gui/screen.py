import pygame
import time
from gui import size, cache
from gui.addon import with_play
from sockets import server

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

def draw_overlay(current_time: float, state):
    if time.time() - state.msg_start_time <= cache.MESSAGE_DISPLAY_TIME and state.msg_text:
        text_surface = font.render(state.msg_text, True, (255,255,255))
        text_rect = text_surface.get_rect(topleft=(10, 10))
        #win.blit(text_surface, text_rect)
        padding = 2
        rect_width = text_rect.width + padding * 2
        rect_height = text_rect.height + padding * 2
        rect_x = text_rect.x - padding
        rect_y = text_rect.y - padding
        rectangle_surface = pygame.Surface((rect_width, rect_height))
        rectangle_surface.fill((0, 0, 0))
        rectangle_surface.set_alpha(128)
        win.blit(rectangle_surface, (rect_x, rect_y))
        win.blit(text_surface, text_rect)

    total_length = vid.duration
    window_width = win.get_size()[0]
    window_height = win.get_size()[1]
    
    pygame.draw.rect(win, (100, 100, 100), 
                    (0, window_height - 5, window_width, 5))
    pygame.draw.rect(win, (255, 0, 0), 
                    (0, window_height - 5, (current_time / total_length) * window_width, 5))
    
def render(vidframe, current_time: float, total_length, state):
    vid.draw(win, (0, 0))
    frame = size.sizeup(vidframe, pygame.display.get_window_size())
    frame_surface = pygame.surfarray.make_surface(frame)
    win.blit(frame_surface, (0, 0))
    draw_overlay(current_time, state)
    if with_play.server:
        server.seek = current_time
    pygame.display.set_caption(f"[{current_time:.2f}s / {total_length:.2f}s] {vid.name}")