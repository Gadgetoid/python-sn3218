from smbus import SMBus

CMD_ENABLE_OUTPUT = 0x00
CMD_ENABLE_LEDS = 0x13
CMD_SET_PWM_VALUES = 0x01
CMD_UPDATE = 0x16

TXT_OUT_OF_RANGE = "Specified output is out of range"
TXT_PWM_INVALID = "Invalid PWM value, must be 0-255"

class sn3218:
	i2c_addr = 0x54
	bus = None
	values = [0x00] * 18
	
	def __init__(self, i2c_bus=1):
		self.bus = SMBus(i2c_bus)

		# Enable output
		self.write(CMD_ENABLE_OUTPUT, 0x01)
		# Enable LEDs ( 0-5, 6-11, 12-17 )
		self.write(CMD_ENABLE_LEDS, [0xFF, 0xFF, 0XFF])

	def setList(self, pins, values):
		if not isinstance(pins, list) and isinstance(values, list):
			for i, v in enumerate(values):
				self.set( (i+pins) % 18, v )
		elif isinstance(pins, list) and isinstance(values, list):
			if len(pins) == len(values):
				for i, v in enumerate(values):
					self.set( pins[i], v)
			else:
				raise ValueError(TXT_LIST_LEN_MISMATCH)
				return False
		elif isinstance(pins, list) and not isinstance(values, list):
			for i, p in enumerate(pins):
				self.set( p, values );
		return True

	def set(self, pin, value):
		if isinstance(value, list) or isinstance(pin, list):
			return self.setList( pin, value )

		if pin > 17 or pin < 0:
			raise ValueError(TXT_OUT_OF_RANGE)
			return False
		if value > 255 or value < 0:
			raise ValueError(TXT_PWM_INVALID)
			return False
		self.values[pin] = value
		return True

	def get(self, pin, value):
		if pin > 17 or pin < 0:
			raise ValueError(TXT_OUT_OF_RANGE)
			return False
		if value > 255 or value < 0:
			raise ValueError(TXT_PWM_INVALID)
			return False
		return self.values[pin]

	def update(self):
		self.write(CMD_SET_PWM_VALUES, self.values)
		self.write(CMD_UPDATE, 0xFF)

	def write(self, reg_addr, value):
		# Treat all writes as block writes
		if not isinstance(value, list):
			value = [value]

		self.bus.write_i2c_block_data(self.i2c_addr, reg_addr, value)

