from smbus import SMBus


addr = 0x8 # bus adress
bus = SMBus(1)

def read_interoceptive_data():
	try:
	    block = bus.read_i2c_block_data(addr, 0, 4)
	    return {"pan_speed": block[0],
	            "pan_pos": block[1],
	            "tilt_speed": block[2],
	            "tilt_pos": block[3]}
	except OSError:
		return {"pan_speed": None,
	            "pan_pos": None,
	            "tilt_speed": None,
	            "tilt_pos": None}


def write_motor_command(motor, pos, speed):
    assert motor in ["pan", "tilt"]
    
    motor_map = {"pan": 0, "tilt": 1}
    
    block = [motor_map[motor], pos, speed]
    bus.write_i2c_block_data(addr, 5, block)