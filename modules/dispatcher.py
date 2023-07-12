from modules.processos import Process


class Dispatcher:
	global_list = []
	ready_list = []
	tracker = 0

	log = 0

	#inicializacao da classe
	def __init__(self, log):
		self.log = log

	def __repr__(self):
		return f'{self.global_list}\n{self.ready_list}'
	
	#lê um arquivo txt com as informaçoes do processo por linha, e coloca os processos na lista global
	def process_parser(self, file):
		processes = open(file,'r').readlines()
		self.global_list = [None]*len(processes)
		self.ready_list = []

		for pid, line in enumerate(processes):
			p = line.split(',')
			self.global_list[pid] = Process(pid, int(p[0]), int(p[1]), int(p[2]),int(p[3]), self.log)
			self.global_list[pid].set_requirements(int(p[4]), int(p[5]), int(p[6]), int(p[7]))
		
		#os processos são organizados por ordem de chegada
		self.global_list.sort(key=lambda process: process.arrival)
		self.tracker = 0
	
	#le um arquivo com informacoes do filesystem e coloca no objeto
	def filesystem_parser(self, file):
		filesystem = open(file,'r').readlines()

	#coloca os processos na fila de pronto e aloca os recursos
	def ready_processess(self, clock, memory_manager, device_manager, scheduler):
		#caso a ordem de chegada de um processo seja maior que o clock, ele quebra
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
