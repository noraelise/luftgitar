import threading
import pygame

import numpy as np

from time import time as now

class MusicPlayer:
    def __init__(self, music_file):
        # Initialize pygame mixer
        pygame.mixer.init(size=32)
        self.music_file = music_file
        self.buffer = np.sin(2 * np.pi * np.arange(44100) * 440 / 44100).astype(np.float32)
        self.sound = pygame.mixer.Sound(self.buffer)
        self.is_playing = False
        self.thread = None
        self.music_started = 0

    def play_music(self):
        if not self.is_playing:
            #pygame.mixer.music.load(self.music_file)
            #pygame.mixer.music.play(-1)  # -1 makes it loop
            self.sound.play(-1)
            self.music_started = now()
            self.is_playing = True

    def start_thread(self):
        if not self.is_playing:
            # Create a new thread each time start is called
            self.thread = threading.Thread(target=self.play_music)
            self.thread.start()

    def stop_thread(self):
        if self.is_playing:
            self.sound.stop()
            self.is_playing = False
            if self.thread is not None:
                self.thread.join()  # Ensure the thread is cleaned up
                self.thread = None  # Reset the thread so it can be recreated


'''
import librosa
from pydub import AudioSegment
from pydub.playback import play
import time

def play_music():
    start_time = time.time()
    play(AudioSegment.from_mp3("music_tracks/smulik.mp3"))
    print("Latency of playback:", time.time() - start_time - 19.7) '''
