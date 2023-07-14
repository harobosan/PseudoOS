from modules.dispatcher import Dispatcher
from modules.filas import Scheduler
from modules.memoria import MemoryManager
from modules.recursos import DeviceManager


if __name__ == '__main__':
    log = 6                         #1
    time_slices = [-1, 2, 4, 8]
    available_memory = 1024         #1024
    reserved_memory = 64            #64
    device_list = ['IMP1','IMP2', 'SCAN', 'MODN', 'SAT1', 'SAT2']

    dispatcher = Dispatcher(log)
    scheduler = Scheduler(time_slices, log)
    memory = MemoryManager(available_memory, reserved_memory, log)
    devices = DeviceManager(device_list, log)

    dispatcher.process_parser('tests/processes.txt')
    files = dispatcher.filesystem_parser('tests/files.txt', 'synchronous')
    if files.mode != 'asynchronous':
        dispatcher.ready_operations()

    clock = 0
    while True:#clock < 31:
        if log > 4:
            print()
            print('----------------------------------------')
            print(f'CYCLE: {clock}')
            print('----------------------------------------')

        dispatcher.ready_processess(clock, memory, devices, scheduler)
        done = not scheduler.execute_processes(dispatcher.arrival_list, memory, devices, files)

        if log > 4:
            print()
            print(f'[ARRIVAL]  > {dispatcher.arrival_list}')
            print(f'[READYING] > {dispatcher.ready_list}')
            print(f'[QUEUES]   > {scheduler}')
            print(f'[DEVICES]  > {devices}')

            if log > 5:
                print(f'[MEMORY]   > {memory}')
                print(f'[STORAGE]  > {files}')

        if done:
            if files.mode == 'asynchronous':
                dispatcher.execute_operations(files)

            if log > 3:
                print()
                print(f'[INFO]     > {clock-1} cycles to finish all processes.')
                print(f'[STORAGE]  > {files}')

            break

        clock += 1
