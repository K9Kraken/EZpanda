import os, builtins
from importlib import import_module, reload as reload_module
import random as pyrandom

from direct.showbase.ShowBase import ShowBase
from panda3d.core import BamCache, AntialiasAttrib, ClockObject, Filename, SamplerState, Shader, PythonTask, BitMask32, MouseButton
from panda3d.core import Vec2, Vec3, Vec4, Point2, Point3, Point4, VBase2, VBase3, VBase4
from panda3d.core import TransparencyAttrib
from panda3d.core import AudioSound
from direct.interval.LerpInterval import LerpPosInterval, LerpHprInterval, LerpFunctionInterval
from direct.interval.IntervalGlobal import Sequence, Parallel
from direct.interval.FunctionInterval import Func, Wait


from scripts.EZpanda.EZnode import Node
from scripts.EZpanda.EZline import Line
from scripts.EZpanda.EZmodel import Model
from scripts.EZpanda.EZactor import Actor
from scripts.EZpanda.EZinstance import SoftInstance, HardInstance
from scripts.EZpanda.EZwindow import Window
from scripts.EZpanda.EZmouse import Mouse
from scripts.EZpanda.EZtext import Text
from scripts.EZpanda.EZcamera import Camera
from scripts.EZpanda.EZtextureBuffer import TextureBuffer
from scripts.EZpanda.EZproceduralMesh import ProceduralMesh
from scripts.EZpanda.EZsound import AudioManager, Audio3DManager, GenSound, GenSound3D
from scripts.EZpanda import EZlights

from panda3d.core import ExecutionEnvironment
PATH = str(Filename.from_os_specific(   ExecutionEnvironment.get_environment_variable("MAIN_DIR")   ))+'/'

#from sys import path
#PATH = path[0] + '/'



class Sound:
    __slots__=()
    BAD = AudioSound.BAD
    READY = AudioSound.READY
    PLAYING = AudioSound.PLAYING

class Transparency:
    __slots__=()
    # No transparency:
    NONE = TransparencyAttrib.M_none
    # Normal transparency, panda will sort back-to-front:
    ALPHA = TransparencyAttrib.M_alpha
    # Assume textures use premultiplied alpha:
    PREMULTIPLIED_ALPHA = TransparencyAttrib.M_premultiplied_alpha
    # Uses ms buffer, alpha values modified to 1.0:
    MULTISAMPLE = TransparencyAttrib.M_multisample
    # Uses ms buffer, alpha values not modified:
    MULTISAMPLE_MASK = TransparencyAttrib.M_multisample_mask
    # Only writes pixels with alpha >= 0.5:
    BINARY = TransparencyAttrib.M_binary
    # Opaque parts first, then sorted transparent parts:
    DUAL = TransparencyAttrib.M_dual


class Interval:
    __slots__=()
    EASE_IN = 'easeIn'
    EASE_OUT = 'easeOut'
    EASE_IN_OUT = 'easeInOut'
    NO_BLEND = 'noBlend'

class Flags:
    __slots__=()
    sound = Sound()
    transparency = Transparency()
    interval = Interval()


class Random:
    __slots__=()

    seed = pyrandom.seed
    float = pyrandom.random
    uniform = pyrandom.uniform
    int = pyrandom.randint
    range = pyrandom.randrange
    choice = pyrandom.choice
    shuffle = pyrandom.shuffle

    def hpr(self, h_angle=360, p_angle=360, r_angle=360):
        return pyrandom.random()*h_angle, pyrandom.random()*p_angle, pyrandom.random()*r_angle

    def point3D(self, xlow, xhigh, ylow, yhigh, zlow, zhigh):
        x = pyrandom.uniform(xlow, xhigh)
        y = pyrandom.uniform(ylow, yhigh)
        z = pyrandom.uniform(zlow, zhigh)
        return x, y, z

    # Return value between 0 and 1.0
    # Value of 1.0 gives a bias to 0.5
    # Lower value gives bias closer to 0
    # Higher value gives bias closer to 1.0
    def bias(self, float_):
        return pow(pyrandom.random(), 1/float_ )

    # Return value between low and high
    # Value of 1.0 with give a equal bias to low high
    # Lower value gives bias closer to low
    # Higher value gives bias closer to high
    def bias_uniform(self, low, high, float_):
        return low + (high-low) * pow(pyrandom.random(), 1/float_ )


class Math:
    __slots__=()

    def distance(self, vector1, vector2):
        v = vector1-vector2
        return v.length()


class Intervals:
    Sequence = Sequence
    Parallel = Parallel

    Func = Func
    Wait = Wait
    __slots__=()

    def pos(self, node, start_pos, end_pos, duration, blend='noBlend', name=None, relative_to=None, fluid=0, bake_in_start=1):
        if relative_to:
            relative_to = relative_to.panda_node
        return LerpPosInterval(node.panda_node, duration, end_pos, startPos=start_pos, other=relative_to, blendType=blend, name=name, fluid=fluid, bakeInStart=bake_in_start)

    def hpr(self, node, start_hpr, end_hpr, duration, blend='noBlend', name=None, relative_to=None, bake_in_start=1):
        if relative_to:
            relative_to = relative_to.panda_node
        return LerpHprInterval(node.panda_node, duration, end_hpr, startHpr=start_hpr, startQuat=None, other=relative_to, blendType=blend, name=name, bakeInStart=bake_in_start)

    def Function(self, func, fr, to, duration, blend='noBlend', args=[], name=None):
        return LerpFunctionInterval(func, fromData=fr, toData=to, duration=duration, blendType=blend, extraArgs=args, name=name)



class Enable: #for ez.enable
    __slots__=()

    def particles(self):
        from scripts.EZpanda.EZparticles import Particles
        ez.panda_showbase.enable_particles()
        ez.particles = Particles()

    def gamepads(self):
        from scripts.EZpanda.EZgamepad import Gamepads
        ez.gamepads = Gamepads()

    def collision(self):
        from scripts.EZpanda.EZcollision import Collision
        ez.collision = Collision()

    def physics(self):
        from scripts.EZpanda.EZphysics import Physics
        ez.physics = Physics()



class Load: #for ez.load
    __slots__=()

    def font(self, filename):
        return loader.load_font( PATH+'fonts/'+filename)

    def sound(self, filename ):
        return ez.audio.load(filename)

    def sound3D(self, filename ):
        return ez.audio3D.load(filename)

    def gen_sound(self, filename, instance_count):
        return GenSound(filename, instance_count)

    def gen_sound3D(self, filename, instance_count):
        return GenSound3D(filename, instance_count)

    def music(self, filename ):
        return ez.music.load(filename)

    def mesh(self, filename ):
        panda_node = loader.load_model( PATH+'meshes/'+filename)
        # With this tag EZ.Model will copy the node when making a model,
        # this way you can keep passing the mesh instead of calling ez.load.mesh every time:
        panda_node.set_tag('copy', '')
        return panda_node

    def texture(self, filename, af=4):
        texture = loader.load_texture( PATH+'textures/'+filename)
        texture.set_minfilter(SamplerState.FT_linear_mipmap_linear)
        texture.set_magfilter(SamplerState.FT_linear_mipmap_linear)
        texture.set_anisotropic_degree(af)
        return texture

    def cursor(self, filename):
        return Filename.binary_filename( PATH+'cursors/'+filename)

    def shader(self, filename ):
        file = Filename( PATH+'shaders/'+filename )
        vert_frag = ["",""]
        with open(file.to_os_specific(), 'r') as data:
            pos = -1
            for line in data:
                if line.strip():
                    if "#version" in line.lower():
                        pos += 1
                    vert_frag[pos] += line
        return Shader.make(Shader.SL_GLSL, vert_frag[0], vert_frag[1])

    def scene(self, name):
        return import_module('scripts.scenes.'+name)




config = {
'file':                       PATH+"config/Config.prc", #Set what config file to use
'window-title':               "EZpanda", #set the window Title
'framebuffer-multisample':    1, #Enable AA, however it is stuck at max, workaround might be to create a new buffer and render to that.
'multisamples':               8,
'win-fixed-size':             1, #Prevent resizing window
'audio-cache-limit':          32, #Set number of simultaneous sounds that can play per a sound manager
'transform-cache':            0, #Disabling this seems to increase speed when moving objects in multiple tests
'want-tk':                    False,
'hardware-animated-vertices': True, #For faster actor animation.
#'threading-model':           'Cull/Draw' #Can get some more speed escept slows down SoftwareInstance.
'want-pstats':                0 #For testing
}


class EZ(dict):

    flags = Flags()

    __slots__=(
        'panda_showbase',
        'is_button_down',
        'run',
        'remove_task',
        '_cam_count',
        'random',
        'math',
        'window',
        'mouse',
        'enable',
        'load',
        'audio',
        'audio3D',
        'music',
        'intervals',
        'gamepads',
        'particles',
        'collision',
        'physics',
        'get_dt',
        '_scene',
        'end',
        'display_region'
        )

    # Setup masks for use in collision, physics, camera:
    mask = {}
    for i in range(0, 32):
        # Adding 1 so the Bitmask will better match the index:
        mask[i+1] = BitMask32.bit(i)
    mask['NONE'] = 0
    mask['ALL'] = BitMask32.all_on()

    PATH = PATH

    # Attatch classes
    Node = Node
    Model = Model
    Actor = Actor
    Line = Line
    SoftInstance = SoftInstance
    HardInstance = HardInstance
    Text = Text
    Camera = Camera
    TextureBuffer = TextureBuffer
    ProceduralMesh = ProceduralMesh
    AudioManager = AudioManager
    Audio3DManager = Audio3DManager

    Vec2 = Vec2
    Vec3 = Vec3
    Vec4 = Vec4
    Point2 = Point2
    Point3 = Point3
    Point4 = Point4
    VBase2 = VBase2
    VBase3 = VBase3
    VBase4 = VBase4

    # Attatch Modules
    lights = EZlights

    def __init__(self, config = config):
        # Add EZ to builtins so it will be global to all modules:
        builtins.ez = self

        # Load the game config file and apply settings:
        from panda3d.core import load_prc_file, load_prc_file_data
        load_prc_file(config['file'])
        for setting in config:
            load_prc_file_data("", setting + " " + str(config[setting]))

        self.panda_showbase = ShowBase()

        # Disable default mouse control over the camera:
        self.panda_showbase.disable_mouse()

        # Class name is misleading, gets keyboard events as well, for realtime key event:
        self.is_button_down = self.panda_showbase.mouseWatcherNode.is_button_down

        self.run = self.panda_showbase.run
        self.remove_task = self.panda_showbase.remove_task

        # Disable cache so updated models will load instead of the cached model, can remove for distrobution:
        BamCache.get_global_ptr().set_active(False)

        # Enable antialiasing:
        render.set_antialias(AntialiasAttrib.MMultisample)
        #render.set_antialias(AntialiasAttrib.MAuto) # Causes white artifacts on edge models

        # Used for giving camera's unique state_keys:
        self._cam_count = 0

        # EZ utils:
        self.random = Random()
        self.math = Math()
        self.window = Window()
        self.mouse = Mouse()
        self.enable = Enable()
        self.load = Load()
        self.audio = AudioManager(self.panda_showbase.sfxManagerList[0])
        self.audio3D = Audio3DManager(self.audio)
        self.music = AudioManager(self.panda_showbase.musicManager)
        self.intervals = Intervals()
        self.gamepads = None
        self.particles = None
        self.collision = None
        self.physics = None

        # Delta time
        self.get_dt = globalClock.get_dt

        # For setting the current scene:
        self._scene = None

        # Start the logic task:
        self.panda_showbase.task_mgr.add(self.logic, 'logic')

        # Call to end the program:
        self.end = self.panda_showbase.userExit

        # Call quit function if system makes panda exit:
        self.panda_showbase.finalExitCallbacks.append( self.quit )

        # Get the default camera's display region:
        self.display_region = self.panda_showbase.camNode.get_display_region(0)

        # Rotate camera2D so aspect2D will us x, y instead of z: (For 2D this is more logical to me)
        self.panda_showbase.camera2d.set_hpr((0,-90,0))

    # This breaks stuff:
    """
    def set_aspect2D(self, x, y, size):
        lens = self.panda_showbase.cam2d.node().get_lens()
        self.panda_showbase.camera2d.set_pos(x, y, 0)
        lens.set_film_size(size, size)
        self.panda_showbase.win.request_properties(self.window.panda_winprops)
    """

    def set_aspect2D_depth(self, bool_):
        self.panda_showbase.aspect2d.set_depth_test(bool_)
        self.panda_showbase.aspect2d.set_depth_write(bool_)

    def make_task(self, function, *args, use_task=True, name='EZtask'):
        task = PythonTask(function, name)
        task.set_args(args, use_task)
        return task

    def add_task(self, task):
        self.panda_showbase.task_mgr.add(task, task.name, extraArgs=task.get_args())

    def add_input_events(self, keys):
        device = 'keyboard'
        for key in keys:
            if MouseButton.is_mouse_button(key):
                device = 'mouse'
            self.panda_showbase.accept(key, self.input_event, [[ device, key, 1 ]])
            key_up = key+'-up'
            self.panda_showbase.accept(key_up, self.input_event, [[ device, key, 0 ]])

    def remove_input_events(self, keys):
        for key in keys:
            self.panda_showbase.ignore(key)
            self.panda_showbase.ignore(key+'-up')

    def reset_scene(self, scene):
        reload_module(scene)

    def set_scene(self, scene):
        # Clear out the current scene if there is one:
        if self._scene:
            self._scene.exit()
            self._scene.render.parent = None
            self._scene.aspect2D.parent = None

        # Add the new scene:
        scene.render.panda_node.reparent_to(self.panda_showbase.render)
        scene.aspect2D.panda_node.reparent_to(self.panda_showbase.aspect2d)
        self.display_region.camera = scene.camera.panda_node
        self._scene = scene
        self._scene.enter()

    def input_event(self, event):
        self._scene.input(event)

    def logic(self, task):
        self._scene.logic(self.get_dt())
        return task.cont

    def quit(self):
        print('EZpanda EXIT')

