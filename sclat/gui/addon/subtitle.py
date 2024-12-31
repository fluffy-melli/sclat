from gui import screen
import gui.font
import pygame

# TODO : Add support for custom subtitle colors
# def hex_to_rgb(hex_color):
#     hex_color = hex_color.lstrip('#')
#     r = int(hex_color[0:2], 16)
#     g = int(hex_color[2:4], 16)
#     b = int(hex_color[4:6], 16)
    
#     return r, g, b

def render(subtitles):
    current_subtitle = []
    for subtitle in subtitles:
        if subtitle['start_time'] <= screen.vid.get_pos() <= subtitle['end_time']:
            current_subtitle.append(subtitle)
        else:
            pass
    for content in current_subtitle:
        #if content['size'] == None:
        #   content['size'] = 25
        #if int(content['size']) > 25:
        #    content['size'] = int(int(content['size']) * 0.75)
        #else:
        #    content['size'] = 25
        content['size'] = 25
        font = gui.font.get(content['size'])
        if '\n' in content['text']:
            i = 0
            for line in (content['text'].split('\n'))[::-1]:
                text_surface = font.render(line, True, (236,82,82))
                text_rect = text_surface.get_rect(center=(screen.win.get_width() * (int(content['position']) / 100), screen.win.get_height() * (int(content['line']) / 100) - (i * (content['size'] + 11))))
                padding = 2
                rect_width = text_rect.width + padding * 2
                rect_height = text_rect.height + padding * 2
                rect_x = text_rect.x - padding
                rect_y = text_rect.y - padding
                rectangle_surface = pygame.Surface((rect_width, rect_height))
                rectangle_surface.fill((0, 0, 0))
                rectangle_surface.set_alpha(128)
                screen.win.blit(rectangle_surface, (rect_x, rect_y))
                screen.win.blit(text_surface, text_rect)
                i += 1
        else:
            text_surface = font.render(content['text'], True, (236,82,82))
            text_rect = text_surface.get_rect(center=(screen.win.get_width() * (int(content['position']) / 100), screen.win.get_height() * (int(content['line']) / 100)))
            padding = 2
            rect_width = text_rect.width + padding * 2
            rect_height = text_rect.height + padding * 2
            rect_x = text_rect.x - padding
            rect_y = text_rect.y - padding
            rectangle_surface = pygame.Surface((rect_width, rect_height))
            rectangle_surface.fill((0, 0, 0))
            rectangle_surface.set_alpha(128)
            screen.win.blit(rectangle_surface, (rect_x, rect_y))
            screen.win.blit(text_surface, text_rect)
    #pygame.display.flip()