class MemoryManager:
	memory = ''
	reserved = 0
	queue = []
	free = 0

	log = 0

	def __init__(self, memory, reserved, log):
		self.memory = '0'*memory
		self.reserved = reserved
		self.free = memory
		self.log = log

	def __repr__(self):
		return '|'+self.memory[:self.reserved]+'|'+self.memory[self.reserved:]+'|'

	def alloc_mem(self, process):
		if process.blocks <= self.free:
			if process.priority:
				segment = self.memory[self.reserved:].split('0'*process.blocks, 1)
				segment[0] = self.memory[:self.reserved]+segment[0]
			else:
				segment = self.memory.split('0'*process.blocks, 1)

			if len(segment) == 2:
				self.memory = segment[0] + '1'*process.blocks + segment[1]
				self.free -= process.blocks
				return len(segment[0])

			if self.log > 2:
				print(f'[WARN] MemoryManager: P{process.pid} requested {process.blocks} blocks, not enough contiguous block were found.')

			self.queue.append(process)
			return -1

		if process.blocks > len(self.memory):
			process.kill = True

			if self.log > 1:
				print()
				print(f'[ERROR] MemoryManager: P{process.pid} requested {process.blocks} blocks, not enough memory in this system.')
				print(f'        Killing Process now.')

			return -1

		elif self.log > 2:
			print(f'[WARN] MemoryManager: P{process.pid} requested {process.blocks} blocks, only {self.free} left.')

		self.queue.append(process)
		return -1

	def free_mem(self, process):
		if self.queue.count(process):
			self.queue.remove(process)
		else:
			self.memory = self.memory[:process.offset] + '0'*process.blocks + self.memory[process.offset+process.blocks:]
			self.free += process.blocks

		if process.offset > 0:

			transfer = []
			for proc in self.queue:
				if proc.blocks <= self.free:
					proc.dormant = False
					transfer.append(proc)

			for proc in transfer:
				self.queue.remove(proc)
