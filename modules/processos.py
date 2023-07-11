class Process:
	pid = 0
	arrival = 0
	priority = 0

	time = 0
	executed = 0
	lifetime = 0

	blocks = 0
	offset = -1

	devices = 0
	dormant = False
	kill = False
	done = False

	log = 0

	def __init__(self, pid, arrival, priority, time, blocks, log):
		self.pid = pid
		self.arrival = arrival
		self.priority = priority
		self.time = time
		self.blocks = blocks
		self.log = log

	def __repr__(self):
		return f'P{self.pid}'

	def execute(self):
		self.executed += 1

		if self.executed == self.time:
			self.done = True

		msg = f'P{self.pid} instruction {self.executed}'
		msg += f' of {self.time}' if self.log > 0 else ''
		print(msg)

	def set_requirements(self, printer, scanner, modem, sata):
		self.devices += sata
		self.devices <<= 1
		self.devices += modem
		self.devices <<= 1
		self.devices += scanner
		self.devices <<= 2
		self.devices += printer

	def alloc_resources(self, memory_manager, device_manager):
		if not self.dormant:
			ready = True

			if self.devices > 0:
				ready = device_manager.reserve_devices(self)

			if ready and self.offset < 0:
				self.offset = memory_manager.alloc_mem(self)
				ready = bool(self.offset >= 0)

			if not ready:
				self.dormant = True

			return ready

		return False

	def free_resources(self, memory_manager, device_manager):
		if self.devices > 0:
			device_manager.release_devices(self)

		if self.offset >= 0:
			memory_manager.free_mem(self)

		if not self.kill:
			print(f'P{self.pid} return SIGINT')

	def print_process(self):
		print()
		print(f'DISPATCHER => P{self.pid}')

		if self.log > 0:
			print(f'       PID     : {self.pid}')
			print(f'       Offset  : {self.offset}')
			print(f'       Blocks  : {self.blocks}')
			print(f'       Priority: {self.priority}')
			print(f'       Time    : {self.time}')
			print(f'       Printer : 1-{bool(self.devices&pow(2,0))}   2-{bool(self.devices&pow(2,1))}')
			print(f'       Scanner : 1-{bool(self.devices&pow(2,2))}')
			print(f'       Modem   : 1-{bool(self.devices&pow(2,3))}')
			print(f'       Drives  : 1-{bool(self.devices&pow(2,4))}   2-{bool(self.devices&pow(2,5))}')
