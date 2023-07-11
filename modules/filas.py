class Scheduler:
	queues = []
	slices = []
	quantum = 0
	start = 1

	log = 0

	def __init__(self, slices, log):
		self.queues = [[] for x in range(len(slices))]
		self.slices = slices
		self.log = log

	def __repr__(self):
		return f'{self.queues}'

	def enqueue_process(self, process):
		self.queues[process.priority].append(process)

	def dequeue_process(self, queue):
		self.start = 1
		return self.queues[queue].pop(0)

	def requeue_process(self, src, dst):
		self.start = 2
		process = self.dequeue_process(src)
		process.priority = dst
		self.enqueue_process(process)

	def execute_processes(self, memory_manager, device_manager):
		for count, queue in enumerate(self.queues):
			if queue:
				if self.start:
					self.start = 0
					print()
					print(f'PROCESS {queue[0].pid} =>')
					msg = f'P{queue[0].pid} '
					msg += 'STARTED' if self.start==1 else 'RESTARTED'
					print(msg)

				executed = queue[0].execute()

				if self.slices[count] > 0:
					self.quantum += 1

				if queue[0].done:
					if self.slices[count] > 0:
						self.quantum = 0
					self.dequeue_process(count).free_resources(memory_manager, device_manager)

				if self.quantum == self.slices[count]:
					self.requeue_process(count, count + 1 if count<len(self.queues)-1 else 0)
					self.quantum = 0

				break
