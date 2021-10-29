# EXAMPLES needs to add parent directory to path so we can import EZ:
import os, sys
sys.path.append(os.path.dirname(__file__) + '/..')

# Disable the creation of python bytecode to keep stuff clean:
sys.dont_write_bytecode = True


from scripts.EZpanda.EZ import EZ, config

config['window-title'] = "EZpanda Examples"

# Setting in custom build of Panda3D, hopefully will be added in master:
config['bullet-split-impulse'] = True

# Load ez with config (ez is added to builtins so is global to all modules):
ez = EZ(config)

# Get the primary display mode aa- w5idth, height, refresh rate:
w, h, r = ez.window.get_display_mode(0)

# lets set a custom window size
w, h = 1024,  768
ez.window.set_display( w, h, r)
ez.window.fullscreen = False



# Enable everything:
ez.enable.gamepads()
ez.enable.particles()
ez.enable.collision()
ez.enable.physics()


# Load a scene and set it:
ez['menu'] = ez.load.scene('menu')
ez.set_scene( ez['menu'] )

ez.run()