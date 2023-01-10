from pygame import mixer


class Sound:
    def __init__(self):
        self.music_channel = mixer.Channel(0)
        self.music_channel.set_volume(0.2)
        self.sfx_channel = mixer.Channel(1)
        self.sfx_channel.set_volume(0.2)

        self.allowSFX = True

        self.soundtrack = mixer.Sound("./src/super_mario_python/sfx/main_theme.ogg")
        self.coin = mixer.Sound("./src/super_mario_python/sfx/coin.ogg")
        self.bump = mixer.Sound("./src/super_mario_python/sfx/bump.ogg")
        self.stomp = mixer.Sound("./src/super_mario_python/sfx/stomp.ogg")
        self.jump = mixer.Sound("./src/super_mario_python/sfx/small_jump.ogg")
        self.death = mixer.Sound("./src/super_mario_python/sfx/death.wav")
        self.kick = mixer.Sound("./src/super_mario_python/sfx/kick.ogg")
        self.brick_bump = mixer.Sound("./src/super_mario_python/sfx/brick-bump.ogg")
        self.powerup = mixer.Sound("./src/super_mario_python/sfx/powerup.ogg")
        self.powerup_appear = mixer.Sound("./src/super_mario_python/sfx/powerup_appears.ogg")
        self.pipe = mixer.Sound("./src/super_mario_python/sfx/pipe.ogg")

    def play_sfx(self, sfx):
        if self.allowSFX:
            self.sfx_channel.play(sfx)

    def play_music(self, music):
        self.music_channel.play(music)
