from modules.processos import Process
from modules.arquivos import FilesystemManager


class Dispatcher:
    #inicializacao da classe
    def __init__(self, log):
        self.arrival_list = []
        self.ready_list = []

        self.pid_list = []
        self.oid_list = []

        self.log = log

    def __repr__(self):
        return f'{self.arrival_list}\n{self.ready_list}'
    
    #lê um arquivo txt com as informaçoes do processo por linha, e coloca os processos na lista global de chegada por ordem de chegada
    def process_parser(self, file):
        processes = open(file,'r').readlines()
        self.pid_list = [None]*len(processes)
        self.ready_list = []

        for pid, line in enumerate(processes):
            p = line.split(', ')
            if len(p) < 2:
                p = line.split(',')

            self.pid_list[pid] = Process(pid, int(p[0]), int(p[1]), int(p[2]),int(p[3]), self.log)
            self.pid_list[pid].set_requirements(int(p[4]), int(p[5]), int(p[6]), int(p[7]))
            self.arrival_list.append(self.pid_list[pid])

        self.arrival_list.sort(key=lambda process: process.arrival)

    #tira os processos da lista de chegada e coloca na lista de prontos
    def ready_processess(self, clock, memory_manager, device_manager, scheduler):
        transfer = []
        for process in self.arrival_list:
            if process.arrival > clock:
                break
            else:
                self.ready_list.append(process)
                transfer.append(process)

        for process in transfer:
            self.arrival_list.remove(process)

        transfer = []
        for process in self.ready_list:
            if process.alloc_resources(memory_manager, device_manager):
                if scheduler.enqueue_process(process):
                    transfer.append(process)
                    process.print_process()

            elif process.kill:
                process.free_resources(memory_manager, device_manager)
                transfer.append(process)

        for process in transfer:
            self.ready_list.remove(process)

    #le um arquivo com informacoes do filesystem e coloca na lista global de operacoes
    def filesystem_parser(self, file, mode):
        filesystem = open(file,'r').readlines()

        file_manager = FilesystemManager(int(filesystem.pop(0)), mode, self.log)

        for i in range(int(filesystem.pop(0))-1,-1,-1):
            line = filesystem.pop(i)
            f = line.split(', ')
            if len(f) < 2:
                f = line.split(',')

            file_manager.set_file(f[0], int(f[1]), int(f[2]))

        for i in range(len(filesystem)):
            line = filesystem[i].split(',')
            oid = len(self.oid_list)
            pid = int(line[0])
            op = int(line[1])
            name = line[2]
            if op:
                blocks = 0
            else:
                blocks = int(line[3])

            self.oid_list.append([oid, pid, op, name[0], blocks])

        return file_manager
    
    #imprime na tela operaçoes 
    def ready_operations(self):
        for operation in self.oid_list:
            if operation[1] < len(self.pid_list):
                self.pid_list[operation[1]].queue_operation(operation)

            else:
                print(f'OPERATION {operation[0]} =>')

                if self.log > 1:
                    mode = 'Delete' if bool(operation[2]) else 'Write'
                    print(f'       OID     : {operation[0]}')
                    print(f'       User    : {operation[1]}')
                    print(f'       Mode    : {mode}')
                    print(f'       File    : {operation[3]}')
                    print(f'       Size    : {operation[4]} blocks')
                    print(f'[ERROR] FileSystem: process does not exist.')
                    print(f'        F{operation[0]} referred to non existing process P{operation[1]}.')

                print(f'F{operation[0]} operation FAILED')
                print()

    #imprime as operacoes e executa
    def execute_operations(self, file_manager):
        for operation in self.oid_list:
            if operation[1] < len(self.pid_list):
                self.pid_list[operation[1]].queue_operation(operation)
                self.pid_list[operation[1]].print_operation(operation)
                self.pid_list[operation[1]].execute_operation(file_manager)
                if self.log > 4:
                    print()
                    print(f'[STORAGE]  > {file_manager}')
                    print()

            else:
                print(f'OPERATION {operation[0]} =>')

                if self.log > 1:
                    mode = 'Delete' if bool(operation[2]) else 'Write'
                    print(f'       OID     : {operation[0]}')
                    print(f'       User    : {operation[1]}')
                    print(f'       Mode    : {mode}')
                    print(f'       File    : {operation[3]}')
                    print(f'       Size    : {operation[4]} blocks')
                    print(f'[ERROR] FileSystem: process does not exist.')
                    print(f'        F{operation[0]} referred to non existing process P{operation[1]}.')

                print(f'F{operation[0]} operation FAILED')

                if self.log > 4:
                    print()
                    print(f'[STORAGE]  > {file_manager}')
                    print()
