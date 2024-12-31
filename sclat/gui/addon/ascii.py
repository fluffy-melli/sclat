import cv2, os
from gui import screen, cache
from gui.addon import with_play
from sockets import server
import pygame

def frame(frame, width=100):
    """
    Converts a given image frame to an ASCII representation.

    Args:
        frame (numpy.ndarray): The input image frame to be converted.
        width (int, optional): The width of the ASCII representation. Defaults to 100.

    Returns:
        list of tuples: A list where each tuple contains two lists:
            - A list of ASCII characters representing a line of the image.
            - A list of RGB color tuples corresponding to each ASCII character.
    """
    height, new_width = frame.shape[:2]
    aspect_ratio = height / new_width
    new_height = int(width * aspect_ratio * 0.55)
    resized_image = cv2.resize(frame, (width, new_height))
    ascii_chars = []
    colors = []
    scale = 256 / len(cache.ASCII_CHARS)
    pixels = resized_image.reshape(-1, 3)
    for pixel in pixels:
        brightness = int(pixel.mean())
        index = int(brightness / scale)
        ascii_chars.append(cache.ASCII_CHARS[index])
        colors.append(tuple(pixel.astype(int)))
    ascii_image = []
    for i in range(0, len(ascii_chars), width):
        line_chars = ascii_chars[i:i+width]
        line_colors = colors[i:i+width]
        ascii_image.append((line_chars, line_colors))
    return ascii_image

def toggle(state):
    """Toggle between ASCII and normal video mode"""
    state.ascii_mode = not state.ascii_mode
    if state.ascii_mode:
        video_width = int(state.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(state.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        ascii_height = int(state.ascii_width * video_height / video_width)
        window_width = state.ascii_width * state.font_size * 0.6
        window_height = int(ascii_height * state.font_size * 0.56)
        screen.win = pygame.display.set_mode((int(window_width), int(window_height)))
        state.font = pygame.font.SysFont("Courier", state.font_size)
    else:
        screen.reset((screen.vid.current_size[0]*1.5, screen.vid.current_size[1]*1.5+5), vid=True)
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def render(vidframe, current_time: float, total_length, state):
    screen.vid.draw(screen.win, (0, 0))
    ascii_frame = frame(vidframe, width=state.ascii_width)
    screen.win.fill((0, 0, 0))
    for i, (line_chars, line_colors) in enumerate(ascii_frame):
        x = 0
        for char, color in zip(line_chars, line_colors):
            color = (color[2], color[1], color[0])
            text_surface = state.font.render(char, False, color)
            screen.win.blit(text_surface, (x, i * state.font_size))
            x += state.font_size * 0.6
    screen.draw_overlay(current_time, state)
    if with_play.server:
        server.seek = current_time
    pygame.display.set_caption(f"[{current_time:.2f}s / {total_length:.2f}s] {screen.vid.name}")