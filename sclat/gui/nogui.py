from moviepy.editor import AudioFileClip
from setting import setting as user_setting
from download import download
import discord_rpc.client
import gui.cache
import pygame,time,os,re

def is_url(url: str) -> bool:
    match = re.search(gui.cache.SEARCH_PATTERN, url)
    return bool(match)
def is_playlist(url: str) -> bool:
    match = re.search(gui.cache.PLAYLIST_SEARCH_PATTERN, url)
    return bool(match)

def run(url:str):
    pygame.init()
    pygame.mixer.init()
    download.clear(user_setting.file_save_dir)
    fn = download.install_nogui(url)
    mp3_path = fn + ".mp3"
    wav_path = fn + ".wav"
    if user_setting.discord_RPC:
        discord_rpc.client.update(time.time(), fn.replace(user_setting.file_save_dir,''))
    if not os.path.exists(mp3_path):
        print(f"Error: MP3 file not found at {mp3_path}")
        return  
    if os.path.getsize(mp3_path) == 0:
        print("Error: Downloaded MP3 file is empty")
        return    
    try:
        audio = AudioFileClip(mp3_path)
        audio.write_audiofile(wav_path, verbose=False, logger=None)
        audio.close()
        if not os.path.exists(wav_path):
            print("Error: WAV conversion failed")
            return
        sound = pygame.mixer.Sound(wav_path)
        sound.play()
        while pygame.mixer.get_busy(): 
            pygame.time.delay(100)
    except Exception as e:
        print(f"Error processing audio: {str(e)}")
    finally:
        gui.cache.video_list.remove(gui.cache.video_list[0])
    
def wait(once):
    while True:
        if len(gui.cache.video_list) == 0:
            if user_setting.discord_RPC:
                discord_rpc.client.update(time.time(),"waiting...")
            print("")
            search = input("Please enter the 'Video Title or URL or Playlist URL' to play the video : ")
        else:
            search = gui.cache.video_list[0]
        if is_playlist(search):
            video_urls = download.get_playlist_video(search)
            gui.cache.video_list.extend(video_urls)
        elif is_url(search):
            gui.cache.video_list.append(search)
        else:
            print("Searching YouTube videos...")
            videos = download.search(search,10)[:5]
            for i, video in enumerate(videos):
                print(f"Choice: {i+1} / Title: {video.title}")
            while True:
                choice = input(f"Choose a videos (1 to {len(videos)}) : ")
                try:
                    int_value = int(choice)
                    if len(videos) < int_value or int_value <= 0:
                        print(f"You can only input from `1` to {len(videos)}")
                        return
                    gui.cache.video_list.append(f"https://www.youtube.com/watch?v={videos[int_value-1].watch_url}")
                    break
                except ValueError:
                    print("The value entered is not an integer")
        trys = 0
        while len(gui.cache.video_list) != 0:
            try:
                run(gui.cache.video_list[0])
                if once:
                    break
            except Exception as e:
                if trys >= 10:
                    print("fail")
                    break
                print(f"An error occurred during playback. Trying again... ({trys}/10) > \n{e}")
                time.sleep(0.5)
                trys += 1