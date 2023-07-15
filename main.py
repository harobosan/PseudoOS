import sys
import time

from modules.dispatcher import Dispatcher
from modules.filas import Scheduler
from modules.memoria import MemoryManager
from modules.recursos import DeviceManager


def read_args(val):
    for i in range(1, len(sys.argv)):
        parameters = sys.argv[i].split('-')
        if parameters[0] == val and len(parameters) > 1:
            parameters.pop(0)
            return parameters

    return None

if __name__ == '__main__':
    log = 6
    if len(sys.argv) > 1:
        arg = read_args('log')
        if arg:
            log = int(arg[0])

    pfile = 'tests/processes.txt'
    if len(sys.argv) > 1:
        arg = read_args('proc')
        if arg:
            pfile = arg[0]

    ffile = 'tests/files.txt'
    if len(sys.argv) > 1:
        arg = read_args('file')
        if arg:
            ffile = arg[0]

    clock_mode = 'time'
    if len(sys.argv) > 1:
        arg = read_args('cmode')
        if arg:
            clock_mode = arg[0]

    file_mode = 'synchronous'
    if len(sys.argv) > 1:
        arg = read_args('fmode')
        if arg:
            file_mode = arg[0]

    time_slices = [0, 1, 1, 2]
    if len(sys.argv) > 1:
        arg = read_args('slices')
        if arg:
            time_slices = [ int(s) for s in arg ]
            time_slices.insert(0, 0)

    available_memory = 1024
    if len(sys.argv) > 1:
        arg = read_args('memory')
        if arg:
            available_memory = int(arg[0])

    reserved_memory = 64
    if len(sys.argv) > 1:
        arg = read_args('reserved')
        if arg:
            reserved_memory = int(arg[0]) if int(arg[0]) < available_memory else available_memory

    device_list = ['IMP1','IMP2', 'SCAN', 'MODN', 'SAT1', 'SAT2']
    if len(sys.argv) > 1:
        arg = read_args('devices')
        if arg:
            device_list = arg

    cycles = 0
    if len(sys.argv) > 1:
        arg = read_args('cycles')
        if arg:
            cycles = int(arg[0])

    dispatcher = Dispatcher(log)
    scheduler = Scheduler(time_slices, clock_mode, log)
    memory = MemoryManager(available_memory, reserved_memory, log)
    devices = DeviceManager(device_list, log)

    dispatcher.process_parser(pfile)
    files = dispatcher.filesystem_parser(ffile, file_mode)
    if files.mode != 'asynchronous':
        dispatcher.ready_operations()

    cycle = 0
    clock = time.time()*1000

    while True if cycles < 1 else bool(cycle < cycles):
        delta = time.time()*1000-clock
        clock += delta

        if log > 4:
            print()
            print('----------------------------------------')
            print(f'CYCLE: {cycle}')
            print(f'DELTA-T: {round(delta,2)}')
            print('----------------------------------------')

        dispatcher.ready_processess(cycle, memory, devices, scheduler)
        incoming = bool(dispatcher.arrival_list) or bool(dispatcher.ready_list)
        if not scheduler.execute_processes(delta, incoming, memory, devices, files):
            if log > 4:
                print()
                print(f'[ARRIVAL]  > {dispatcher.arrival_list}')
                print(f'[READYING] > {dispatcher.ready_list}')
                print(f'[QUEUES]   > {scheduler}')
                print(f'[DEVICES]  > {devices}')

                if log > 5:
                    print(f'[MEMORY]   > {memory}')
                    print(f'[STORAGE]  > {files}')

        else:
            if log > 3:
                print()
                print(f'[INFO]     > {cycle} cycles to finish all processes.')

            if files.mode == 'asynchronous':
                print()
                dispatcher.execute_operations(files)
                print()
            else:
                print(f'[STORAGE]  > {files}')
                print()

            break

        cycle += 1
