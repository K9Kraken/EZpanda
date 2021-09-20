import os, builtins
from importlib import import_module, reload as reload_module
import random as pyrandom

from direct.showbase.ShowBase import ShowBase
from panda3d.core import BamCache, AntialiasAttrib, ClockObject, Filename, SamplerState, Shader, PythonTask, BitMask32, MouseButton
from panda3d.core import Vec2, Vec3, Vec4, Point2, Point3, Point4, VBase2, VBase3, VBase4

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
from scripts.EZpanda.EZsound import AudioManager, Audio3DManager
from scripts.EZpanda import EZlights


from panda3d.core import ExecutionEnvironment
PATH = ExecutionEnvironment.get_environment_variable("MAIN_DIR")+'/'


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
'file':                       "config/Config.prc", #Set what config file to use
'window-title':               "EZpabda", #set the window Title
'framebuffer-multisample':    1, #Enable AA, however it is stuck at max, workaround might be to create a new buffer and render to that.
'multisamples':               8,
'win-fixed-size':             1, #Prevent resizing window
'audio-cache-limit':          32, #Set number of simultaneous sounds that can play per a sound manager
'transform-cache':            0, #Disabling this seems to increase speed when moving objects in multiple tests
'want-tk':                    False,
'hardware-animated-vertices': True, #For faster actor animation.
#'threading-model':           'Cull/Draw', #Can get some more speed escept slows down SoftwareInstance.
'want-pstats':                0 #For testing
}


class EZ(dict):
    __slots__=(
        'is_button_down',
        'run',
        'remove_task',
        '_cam_count',
        'random',
        'window',
        'mouse',
        'enable',
        'load',
        'audio',
        'audio3D',
        'music',
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
    for i in range(0, 31):
        mask[i+1] = BitMask32.bit(i)
    mask['NONE'] = 0
    mask['ALL'] = BitMask32.all_on()

    PATH = PATH

    # Attatch classes
    Node = Node
    Line = Line
    Model = Model
    Actor = Actor
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

    panda_showbase = ShowBase()

    def __init__(self, config = config):
        # Add EZ to builtins so it will be global to all modules:
        builtins.ez = self

        # Load the game config file and apply settings:
        from panda3d.core import load_prc_file, load_prc_file_data
        load_prc_file(config['file'])
        for setting in config:
            load_prc_file_data("", setting + " " + str(config[setting]))

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
        self.window = Window()
        self.mouse = Mouse()
        self.enable = Enable()
        self.load = Load()
        self.audio = AudioManager(self.panda_showbase.sfxManagerList[0])
        self.audio3D = Audio3DManager(self.audio)
        self.music = AudioManager(self.panda_showbase.musicManager)
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