from modules.processos import Process
from modules.filas import enqueue_process, execute_processes

#Debugging
from modules.filas import print_queues
from modules.memoria import print_mem
from modules.recursos import print_resources

def asort(process):
	return process.arrival

def sort_by_arrival(process_list):
	process_list.sort(key=asort)

def ready_processess(clock, ready_list):
	i = 0

	for process in ready_list:
		if process.arrival > clock:
			break

		if process.alloc_resources():
			enqueue_process(process)
			process.print_process()
			ready_list.pop(i)
			i -= 1

		i += 1

def process_parser(file, global_list, ready_list):
	processes = open(file,'r').readlines()

	pid = 0
	for line in processes:
		p = line.split(',')
		global_list[pid] = Process(pid, int(p[0]), int(p[1]), int(p[2]),int(p[3]))
		global_list[pid].set_requirements(int(p[4]), int(p[5]), int(p[6]), int(p[7]))
		ready_list.append(global_list[pid])
		pid += 1

	sort_by_arrival(ready_list)

def filesystem_parser(file):
	filesystem = open(file,'r').readlines()

def cpu_cycle(clock, ready_list):
	#print(clock)
	ready_processess(clock, ready_list)
	#print(ready_list)
	#print_queues()
	#print_mem()
	#print_resources()
	execute_processes(clock)
	#print(" ")

if __name__ == '__main__':
	global_list = [None] * 10
	ready_list = []

	process_parser("processes.txt", global_list, ready_list)

	clock = 0
	while clock < 30:
		cpu_cycle(clock, ready_list)
		clock += 1
