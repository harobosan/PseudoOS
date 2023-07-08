from modules.memoria import alloc_mem, free_mem
from modules.recursos import reserve_resources, release_resources

class Process:
	pid = 0
	arrival = 0
	priority = 0

	time = 0
	executed = 0
	lifetime = 0

	blocks = 0
	offset = -1

	resources = 0

	done = False

	def __init__(self, pid, arrival, priority, time, blocks):
		self.pid = pid
		self.arrival = arrival
		self.priority = priority
		self.time = time
		self.blocks = blocks

	def __repr__(self):
		return "P"+str(self.pid)

	def execute(self):
		self.executed += 1
		print("P"+str(self.pid)+" instruction "+str(self.executed)+" of "+str(self.time))

		if self.executed == self.time:
			self.done = True

	def set_requirements(self, printer, scanner, modem, sata):
		self.resources += printer
		self.resources <<= 1
		self.resources += scanner
		self.resources <<= 1
		self.resources += modem
		self.resources <<= 2
		self.resources += sata

	def alloc_resources(self):
		is_ready = True

		if self.resources > 0:
			is_ready = reserve_resources(self.pid, self.resources)

		if is_ready:
			if self.offset < 0:
				self.offset = alloc_mem(self.blocks, self.priority)
				is_ready = bool(self.offset >= 0)

		return is_ready

	def free_resources(self):
		if self.resources > 0:
			release_resources(self.resources)

		if self.offset >= 0:
			free_mem(self.blocks, self.offset)

		print("P"+str(self.pid)+" return SIGINT")

	def print_process(self):
		print("DISPATCHER => " + str(self.pid))
