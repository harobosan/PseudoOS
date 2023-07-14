from modules.processos import Process
from modules.arquivos import FilesystemManager

class Dispatcher:
    '''
    Dispatcher

    pid_list= lista global de processos
    oid_list= lista global de operações
    arrival_list= fila de chegada de processos para a CPU
    ready_list= list de processos em espera por recursos
    log= nível de verbose
    '''

    def __init__(self, log):
        self.pid_list = []
        self.oid_list = []

        self.arrival_list = []
        self.ready_list = []

        self.log = log

    def __repr__(self):
        return f'{self.arrival_list}\n{self.ready_list}'

    def process_parser(self, file):
        '''
        process_parser(self, file)

        lê um arquivo de path 'file', gera processos à partir das linhas
        formatadas do arquivo e armazena os processos na lista global pid_list
        '''
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

    def ready_processess(self, clock, memory_manager, device_manager, scheduler):
        '''
        ready_processess(self, clock, memory_manager, device_manager, scheduler)

        move os processos que chegam à CPU para a fila de preparo no ciclo 'clock',
        remove processos mortos na fila preparo e tenta alocar recursos rquisitados
        pelos processos na fila para movê-los para a fila de execução quando prontos
        '''

        transfer = []
        for process in self.arrival_list:
            if process.arrival > clock:
                break

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

    def filesystem_parser(self, file, mode):
        '''
        filesystem_parser(self, file, mode)

        lê um arquivo de path 'file', gera operações de arquivo em disco à partir das linhas
        formatadas do arquivo, armazena os processos na lista global oid_list e cria um
        objeto de gerenciador de sistema de arquivos com o modo de operação 'mode' e
        especificações encontradas em 'file'

        retorna: objeto gerenciador de sistema de arquivos
        '''
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

    def ready_operations(self):
        '''
        ready_operations(self)

        prepara as operações na lista global oid_list associando estas com
        seus respectivos processos
        '''

        for operation in self.oid_list:
            if operation[1] < len(self.pid_list):
                self.pid_list[operation[1]].queue_operation(operation)

            else:
                self.print_operation(operation)

                if self.log > 1:
                    print('[ERROR] FileSystem: process does not exist.')
                    msg = f'        F{operation[0]} referred to non existing process'
                    msg += f' P{operation[1]}.'
                    print(msg)

                print(f'F{operation[0]} operation FAILED')
                print()

    def execute_operations(self, file_manager):
        '''
        execute_operations(self, file_manager)

        executa todas as operações na lista global oid_list em ordem, a ser usado
        quando gerenciar sistema de arquivos 'file_manager' estiver em modo
        'asynchronous'
        '''

        for operation in self.oid_list:
            if operation[1] < len(self.pid_list):
                self.pid_list[operation[1]].queue_operation(operation)
                self.pid_list[operation[1]].execute_operation(file_manager)

                if self.log > 4:
                    print()
                    print(f'[STORAGE]  > {file_manager}')
                    print()

            else:
                self.print_operation(operation)

                if self.log > 1:
                    print('[ERROR] FileSystem: process does not exist.')
                    msg = f'        F{operation[0]} referred to non existing process'
                    msg += f' P{operation[1]}.'
                    print(msg)

                print(f'F{operation[0]} operation FAILED')
                print()

                if self.log > 4:
                    print()
                    print(f'[STORAGE]  > {file_manager}')
                    print()

    def print_operation(self, operation):
        '''
        print_operation(self, operation)

        exibe informações basicas de uma operação no terminal
        '''

        print(f'OPERATION {operation[0]} =>')

        if self.log > 1:
            mode = 'Delete' if bool(operation[2]) else 'Write'
            print(f'       OID     : {operation[0]}')
            print(f'       User    : {operation[1]}')
            print(f'       Mode    : {mode}')
            print(f'       File    : {operation[3]}')
            print(f'       Size    : {operation[4]} blocks')
