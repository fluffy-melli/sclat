import os,pygame,shutil,yt_dlp
from pytubefix import YouTube,Search
from pytubefix.cli import on_progress
####################################
from src.utils import user_setting, subtitles
import xml.etree.ElementTree as ET
import src.utils
import src.utils.user_setting
import src.win.screen

def convert_size(bytes):
    for unit in ['Byte', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    on_progress(stream, chunk, bytes_remaining)
    src.win.screen.load = 1
    
    width = stream.width if stream.width else 800
    height = stream.height if stream.height else 600
    width = width * 1.5
    height = height * 1.5
    
    src.win.screen.reset((width, height+5))
    pygame.display.set_caption(f"Downloading: {convert_size(bytes_downloaded)} of {convert_size(total_size)} ({percentage:.2f}%)")
    text_surface = src.win.screen.font.render(f"Downloading: {convert_size(bytes_downloaded)} of {convert_size(total_size)} ({percentage:.2f}%)", True, (255,255,255))
    text_rect = text_surface.get_rect(center=(int(width/2), int(height/2)))
    src.win.screen.win.blit(text_surface, text_rect)
    pygame.display.update()

def progress_hook(d):
    try:
        width = src.win.screen.win.get_size()[0]
        height = src.win.screen.win.get_size()[1]
        src.win.screen.win.fill((0,0,0))
        pygame.display.set_caption(f"Downloading: {d['_percent_str']} of {d['_speed_str']} - ETA: {d['_eta_str']}")
        text_surface = src.win.screen.font.render(f"Downloading: {d['_percent_str']} of {d['_speed_str']} - ETA: {d['_eta_str']}", True, (255,255,255))
        text_rect = text_surface.get_rect(center=(int(width/2), int(height/2)))
        src.win.screen.win.blit(text_surface, text_rect)
        pygame.display.update()
    except Exception as e:
        print(e)

def after(a,b):
    src.win.screen.load = 2

def search(q:str,result:int):
    list = Search(query=q)
    return list.videos

def get_playlist_video(playlist_url):
    ydl_opts = {
        'extract_flat': True,
        'force_generic_extractor': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        if 'entries' in result:
            return [entry['url'] for entry in result['entries']]
        else:
            return []

def search_infos(videos):
    res = []
    for video in videos:
        res.append(video_info(f"https://www.youtube.com/watch?v={video.watch_url}"))
    return res

def video_info(url:str):
    return YouTube(url).streaming_data

def install(url:str):
    os.makedirs(user_setting.file_save_dir, exist_ok=True)
    yt = YouTube(url, on_progress_callback = progress_function, on_complete_callback=after)
    fns = f"{user_setting.file_save_dir}/{yt.length}/"
    os.makedirs(fns, exist_ok=True)
    if not os.path.exists(fns):
        os.makedirs(fns)
    fn = f"{fns}/{yt.title}.mp4"
    yt = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    yt.download(filename=fn)
    sr = install_srt(url, fns, yt.title, src.utils.user_setting.SubTitle)
    return fns, fn, sr

def install_nogui(url:str):
    os.makedirs(user_setting.file_save_dir, exist_ok=True)
    yt = YouTube(url, on_progress_callback=on_progress)
    fn = f"{user_setting.file_save_dir}/{yt.title}"
    audio = yt.streams.filter(only_audio=True).first()
    audio.download(filename=fn+".mp3")
    return fn

def install_srt(url: str, fns: str, title: str, lang = 'ko'):
    if lang == '' or lang == 'none':
        return None
    ydl_opts = {
        'writesubtitles': True,
        'subtitleslangs': [lang],
        'writeautomaticsub': True,
        'outtmpl': f'{fns}/{title}.%(ext)s',
        'skip_download': True,
        'progress_hooks': [progress_hook],
        'verbose': False,
        'logger': None,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f'{fns}/{title}.{lang}.vtt'
    except Exception as e:
        return None

def clear(folder_path):
    if os.path.exists(folder_path):
        if os.path.isdir(folder_path):
            shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

