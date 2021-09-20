#Stop python form creating bytecode to keep stuff clean:
import sys; sys.dont_write_bytecode = True


from scripts.EZpanda.EZ import EZ, config

config['window-title'] = "EZpanda"

#ez will be global to all moduls:
ez = EZ(config)


#Get the primary display mode - width, height, refresh rate:
w, h, r = ez.window.get_display_mode(0)
w, h = 1024, 768
ez.window.set_display( w, h, r)

ez.enable.gamepads()
ez.enable.particles()
ez.enable.collision()
ez.enable.physics()


ez['menu'] = ez.load.scene('menu')
ez.set_scene( ez['menu'] )


ez.run()