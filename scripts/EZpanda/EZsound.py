from direct.showbase.Audio3DManager import Audio3DManager as PandaAudio3DManager
from panda3d.core import AudioManager as PandaAudioManager



class Sound:
    __slots__=(
        '_audio_manager',
        'panda_sound',
        'play',
        'stop',
        'get_status',
        'get_length'
        )

    def __init__(self, panda_sound):
        self.panda_sound = panda_sound

        self.play = panda_sound.play
        self.stop = panda_sound.stop
        self.get_status = panda_sound.status
        self.get_length = panda_sound.length

    @property
    def loop(self):
        return self.panda_sound.get_loop()
    @loop.setter
    def loop(self, value):
        self.panda_sound.set_loop(value)

    @property
    def volume(self):
        return self.panda_sound.get_volume()
    @volume.setter
    def volume(self, value):
        self.panda_sound.set_volume(value)

    @property
    def time(self):
        return self.panda_sound.get_time()
    @time.setter
    def time(self, value):
        self.panda_sound.set_time(value)

    @property
    def rate(self):
        return self.panda_sound.get_play_rate()
    @rate.setter
    def rate(self, value):
        self.panda_sound.set_play_rate(value)



class Sound3D(Sound):
    __slots__=(
        '_audio_manager',
        '_node'
        )

    def __init__(self, panda_sound3D, audio_manager):
        Sound.__init__(self, panda_sound3D)
        self._audio_manager = audio_manager
        self._node = None

    @property
    def node(self):
        return self._parent
    @node.setter
    def node(self, node):
        if node:
            self._audio_manager.attach_sound_to_object(self.panda_sound, node.panda_node)
            self._node = node
        else:
            self._audio_manager.detach_sound(self.panda_sound)
            self._node = None




class GenSound:
    def __init__(self, file_name, instance_count):
        self.sounds = []
        self.count = 0
        self.limit = instance_count - 1
        for i in range(instance_count):
            self.sounds.append( ez.load.sound(file_name) )

    def play(self):
        self.sounds[self.count].play()
        self.count += 1
        if self.count > self.limit:
            self.count = 0

    def set_volume(self, float_):
        for sound in self.sounds:
            sound.volume = float_



class GenSound3D:
    def __init__(self, file_name, instance_count):
        self.sounds = []
        self.count = 0
        self.limit = instance_count - 1
        for i in range(instance_count):
            self.sounds.append( ez.load.sound3D(file_name) )

    def play(self):
        self.sounds[self.count].play()
        self.count += 1
        if self.count > self.limit:
            self.count = 0

    def play_on(self, node):
        sound = self.sounds[self.count]
        sound.node = node
        sound.play()
        self.count += 1
        if self.count > self.limit:
            self.count = 0

    def play_av_on(self, node):
        for sound in self.sounds:
            if sound.get_status() == ez.flags.sound.READY:
                sound.node = node
                sound.play()
                break

    def set_node(self, node):
        for sound in sounds:
            sound.node = node

    def set_volume(self, float_):
        for sound in self.sounds:
            sound.volume = float_



class AudioManager:
    __slots__=(
        'panda_audio'
        )

    def __init__(self, panda_audio=None):
        if panda_audio:
            self.panda_audio=panda_audio
        else:
            self.panda_audio=PandaAudioManager.createAudioManager()
            ez.panda_showbase.add_sfx_manager(self.panda_audio)

    def load(self, filename):
        return Sound(self.panda_audio.get_sound( ez.PATH+'sounds/'+filename ))

    @property
    def volume(self):
        return self.panda_audio.get_volume()
    @volume.setter
    def volume(self, float_):
        self.panda_audio.set_volume(min(1.0, float_))

    @property
    def concurrent_limit(self):
        return self.panda_audio.get_concurrent_sound_limit()
    @concurrent_limit.setter
    def concurrent_limit(self, int_):
        self.panda_audio.set_concurrent_sound_limit(int_)

    def stop_all_sounds(self):
        self.panda_audio.stop_all_sounds()



class Audio3DManager(AudioManager):
    __slots__=(
        '_listener'
        )

    def __init__(self, audio_manager):
        AudioManager.__init__(self, PandaAudio3DManager(audio_manager.panda_audio))
        self._listener = None

    def load(self, filename):
        return Sound3D(self.panda_audio.load_sfx( ez.PATH+'sounds/'+filename ), self.panda_audio)

    @property
    def listener(self):
        return self._listener
    @listener.setter
    def listener(self, node):
        if node:
            self.panda_audio.attach_listener(node.panda_node)
            self._listener = node
        else:
            self.panda_audio.remove_listener()
            self._listener = None

    @property
    def distance_factor(self):
        return self.panda_audio.get_distance_factor()
    @distance_factor.setter
    def distance_factor(self, value):
        self.panda_audio.set_distance_factor(value)

    @property
    def drop_off_factor(self):
        return self.panda_audio.get_drop_off_factor()
    @drop_off_factor.setter
    def drop_off_factor(self, value):
        self.panda_audio.set_drop_off_factor(value)