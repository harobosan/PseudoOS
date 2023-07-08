from modules.processos import Process

queues = [[],[],[],[]]
quantum = 0

def enqueue_process(process):
	queues[process.priority].append(process)

def dequeue_process(queue):
	return queues[queue].pop(0)

def requeue_process(src, dst):
	process = dequeue_process(src)
	process.priority = dst
	enqueue_process(process)

def execute_processes(clock):
	global quantum
	if queues[0]:
		queues[0][0].execute()
		if queues[0][0].done:
			dequeue_process(0).free_resources()

	elif queues[1]:
		queues[1][0].execute()
		quantum += 1

		if queues[1][0].done:
			dequeue_process(1).free_resources()
			quantum = 0

		if quantum == 2:
			requeue_process(1,2)
			quantum = 0

	elif queues[2]:
		queues[2][0].execute()
		quantum += 1

		if queues[2][0].done:
			dequeue_process(2).free_resources()
			quantum = 0

		if quantum == 4:
			requeue_process(2,3)
			quantum = 0

	elif queues[3]:
		queues[3][0].execute()
		quantum += 1

		if queues[3][0].done:
			dequeue_process(3).free_resources()
			quantum = 0

		if quantum == 8:
			requeue_process(3,3)
			quantum = 0

def print_queues():
	print(queues)
