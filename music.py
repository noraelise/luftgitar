from pygame import mixer

class MusicPlayer:
    def __init__(self, music_file):
        # Initialize pygame mixer
        self.music_file = music_file
        self.is_playing = False
        
        mixer.init()
        mixer.music.load(self.music_file)

    def play_music(self):
        if not self.is_playing:
            mixer.music.play(-1)  # -1 makes it loop
            self.is_playing = True

    def stop_music(self):
        if self.is_playing:
            mixer.music.stop()
            self.is_playing = False