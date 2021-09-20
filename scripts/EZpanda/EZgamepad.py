from panda3d.core import InputDevice



class Math:
    __slots__=()

    def range_to_percent( x, min, max):
        x2 = abs(x)
        return (x2 - min) / (max - min) * (x2/x)

    def range_to_limit( x, low, high):
        x = clamp(abs(x), low, high)
        x2 = abs(x)
        return (x2 - low) / (high - low) * (x2/x)



class Gamepad:
    __slots__=(
        'name',
        'number',
        'device',
        'axis_min',
        'axis_max',
        'has_rumble'
        )

    def __init__(self, name, device):
        self.name = name
        self.number = None
        self.device = device
        self.axis_min = 0.12
        self.axis_max = 0.70
        self.has_rumble = device.has_feature(device.Feature.vibration)



class Gamepads:
    __slots__=(
        '_gamepads'
        )

    InputDevice = InputDevice

    def __init__(self):

        self._gamepads = self.setup_gamepads()

        ez.panda_showbase.task_mgr.add(self.task_gamepad, 'gamepads')
        ez.panda_showbase.accept('connect-device', self.device_connected)
        ez.panda_showbase.accept('disconnect-device', self.device_disconnected)

    def __getitem__(self, item):
        return self._gamepads[item]

    def __bool__(self):
        if self._gamepads:
            return True
        else:
            return False

    def device_connected(self, device):
        devices = ez.panda_showbase.devices.get_devices(self.InputDevice.DeviceClass.gamepad)
        if device in devices:
            in_gamepads = False
            for gamepad in self._gamepads:
                if gamepad.device.serial_number == device.serial_number:
                    in_gamepads = True
                    gamepad.device = device
                    self.register_gamepad(gamepad)
                    ez.input_event([gamepad.name, 'CONNECTED', 1])
            if in_gamepads == False:
                number = len(self._gamepads)
                name = 'gamepad' + str(number)
                gamepad = Gamepad(name, device)
                gamepad.number = number
                self._gamepads.append(gamepad)
                self.register_gamepad(gamepad)
                ez.input_event([gamepad.name, 'NEW_CONNECTED', 1])

    def device_disconnected(self, device):
        for gamepad in self._gamepads:
            if gamepad.device == device:
                ez.panda_showbase.detach_input_device(device)
                ez.input_event([gamepad.name, 'DISCONNECTED', 1])

    def register_gamepad(self, gamepad):
        ez.panda_showbase.attach_input_device(gamepad.device, prefix=gamepad.name)
        for button in gamepad.device.buttons:
            ez.panda_showbase.accept(gamepad.name+'-'+button.handle.name, ez.input_event, [ [gamepad.name, button.handle.name, 1] ])
            ez.panda_showbase.accept(gamepad.name+'-'+button.handle.name+'-up', ez.input_event, [ [gamepad.name, button.handle.name, 0] ])

    def setup_gamepads(self):
        gamepads = []
        devices = ez.panda_showbase.devices.get_devices(self.InputDevice.DeviceClass.gamepad)
        for device in devices:
            number = len(gamepads)
            name = "gamepad" + str(number)
            gamepad = Gamepad(name, device)
            gamepad.number = number
            gamepads.append(gamepad)
            self.register_gamepad(gamepad)
        return gamepads

    def task_gamepad(self, task):
        for gamepad in self._gamepads:
            for axis in gamepad.device.axes:
                if abs(axis.value) > gamepad.axis_min:
                    value = Math.range_to_limit(axis.value, gamepad.axis_min, gamepad.axis_max) #Convert axis value between 0 and 1
                    ez.input_event([gamepad.name, axis.axis.name, value])
        return task.cont