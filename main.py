from modules.dispatcher import Dispatcher
from modules.filas import Scheduler
from modules.memoria import MemoryManager
from modules.recursos import DeviceManager


if __name__ == '__main__':
	log = 3						#1
	time_slices = [-1, 2, 4, 8]
	available_memory = 16 		#1024
	reserved_memory = 8 		#64
	device_list = ['IMP1','IMP2', 'SCAN', 'MODN', 'SAT1', 'SAT2']

	dispatcher = Dispatcher(log)
	scheduler = Scheduler(time_slices, log)
	memory = MemoryManager(available_memory, reserved_memory, log)
	devices = DeviceManager(device_list, log)

	dispatcher.process_parser("processes.txt")

	clock = 0
	while clock < 31:
		if log > 2:
			print()
			print('----------------------------------------')
			print(f'CYCLE: {clock}')
			print('----------------------------------------')

		dispatcher.ready_processess(clock, memory, devices, scheduler)
		scheduler.execute_processes(memory, devices)

		if log > 2:
			print()
			print(f'[READYING] > {dispatcher.ready_list}')
			print(f'[QUEUES]   > {scheduler}')
			print(f'[DEVICES]  > {devices}')
			if log > 3:
				print(memory)

		clock += 1
