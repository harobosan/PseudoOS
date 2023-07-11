from modules.processos import Process


class Dispatcher:
	global_list = []
	ready_list = []
	tracker = 0

	log = 0

	def __init__(self, log):
		self.log = log

	def __repr__(self):
		return f'{self.global_list}\n{self.ready_list}'

	def process_parser(self, file):
		processes = open(file,'r').readlines()
		self.global_list = [None]*len(processes)
		self.ready_list = []

		for pid, line in enumerate(processes):
			p = line.split(',')
			self.global_list[pid] = Process(pid, int(p[0]), int(p[1]), int(p[2]),int(p[3]), self.log)
			self.global_list[pid].set_requirements(int(p[4]), int(p[5]), int(p[6]), int(p[7]))

		self.global_list.sort(key=lambda process: process.arrival)
		self.tracker = 0

	def filesystem_parser(self, file):
		filesystem = open(file,'r').readlines()

	def ready_processess(self, clock, memory_manager, device_manager, scheduler):
		for t in range(self.tracker, len(self.global_list)):
			if self.global_list[t].arrival > clock:
				break
			else:
				self.ready_list.append(self.global_list[t])
				self.tracker = t+1

		transfer = []
		for process in self.ready_list:
			if process.alloc_resources(memory_manager, device_manager):
				scheduler.enqueue_process(process)
				transfer.append(process)
				process.print_process()
			elif process.kill:
				process.free_resources(memory_manager, device_manager)
				transfer.append(process)

		for process in transfer:
			self.ready_list.remove(process)
