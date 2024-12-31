import pygame
import numpy as np
import pygame.sndarray
from pydub import AudioSegment
from gui import screen

sample_rate = 22050
buffer_size = 1024
channels = 2

def run(audio_data):
    audio_index = int(screen.vid.get_pos() / screen.vid.duration * len(audio_data))
    if audio_index + buffer_size < len(audio_data):
        audio_chunk = audio_data[audio_index:audio_index + buffer_size]
    else:
        audio_chunk = audio_data[audio_index:]
    fft_data = np.fft.fft(audio_chunk)
    audio_index += buffer_size
    if audio_index >= len(audio_data):
        audio_index = 0
    plot_spectrum(fft_data, audio_chunk)

def plot_spectrum(fft_data, audio_chunk):
    if np.max(fft_data) == 0j:
        return
    amplitude = np.abs(fft_data)
    amplitude = np.nan_to_num(amplitude)
    amplitude[amplitude < 1e-10] = 0
    fft_freq = np.fft.fftfreq(len(audio_chunk), 1 / sample_rate)
    half_n = len(fft_freq) // 2
    frequencies = fft_freq[:half_n]
    amplitudes = amplitude[:half_n]
    width = screen.win.get_width()
    height = screen.win.get_height() - 5
    max_amplitude = np.max(amplitudes)
    for i, amp in enumerate(amplitudes):
        x = int(i * width / len(frequencies))
        y = int(height - (amp / max_amplitude) * height / 2)
        if x < width // 3:
            r = int(255 * (1 - x / (width // 3)))
            g = int(255 * (x / (width // 3)))
            b = 0
        elif x < 2 * width // 3:
            r = 0
            g = int(255 * (1 - (x - width // 3) / (width // 3)))
            b = int(255 * ((x - width // 3) / (width // 3)))
        else:
            r = 0
            g = 0
            b = 255
        color = pygame.Color(r, g, b)
        pygame.draw.line(screen.win, color, (x, height), (x, y), width = 2)

def extract_audio_from_video(video_file):
    audio = AudioSegment.from_file(video_file, format="mp4")
    audio = audio.set_channels(1)
    audio = audio.set_frame_rate(22050)
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    return audio_data