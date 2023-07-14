class Process:
    '''
    Processo

    pid= identificador único do processo
    arrival= ciclo de chegada na CPU
    priority= prioridade de execução
    executed= quantidade de instruções ja executadas
    blocks= quantidade de blocos de memória necessários
    offset= posição de memória alocada
    devices= bitmap de dispositivos necessários
    operations= fila de operações de arquivos do processo
    dormant= flag de estado
    kill= flag de estado
    done= flag de estado
    log= nível de verbose
    '''

    def __init__(self, pid, arrival, priority, time, blocks, log):
        self.pid = pid
        self.arrival = arrival
        self.priority = priority

        self.time = time
        self.executed = 0
        #self.lifetime = 0

        self.blocks = blocks
        self.offset = -1

        self.devices = 0
        self.operations = []

        self.dormant = False
        self.kill = False
        self.done = False

        self.log = log

    def __repr__(self):
        return f'P{self.pid}'

    def set_requirements(self, printer, scanner, modem, sata):
        '''
        set_requirements(self, printer, scanner, modem, sata)

        define o bitmap de dispositivos necessários do processo
        '''

        self.devices += sata
        self.devices <<= 1
        self.devices += modem
        self.devices <<= 1
        self.devices += scanner
        self.devices <<= 2
        self.devices += printer

    def alloc_resources(self, memory_manager, device_manager):
        '''
        alloc_resources(self, memory_manager, device_manager)

        requisita a alocação de recursos para o processo ao gerenciador
        de memória 'memory_manager' e gerenciador de dispositivos 'device_manager'

        retorna: bool se conseguiu alocar todos os recursos que o processo precisa
        '''

        if not self.dormant:
            ready = True

            if self.devices > 0:
                ready = device_manager.reserve_devices(self)

            if ready and self.offset < 0:
                self.offset = memory_manager.alloc_mem(self)
                ready = bool(self.offset >= 0)

            if not ready:
                self.dormant = True

            return ready

        return False

    def free_resources(self, memory_manager, device_manager):
        '''
        free_resources(self, memory_manager, device_manager)

        requisita a liberação dos recursos alocados pelo processo ao gerenciador
        de memória 'memory_manager' e gerenciador de dispositivos 'device_manager'
        '''

        if self.devices > 0:
            device_manager.release_devices(self)

        if self.offset >= 0:
            memory_manager.free_mem(self)

        if not self.kill:
            print(f'P{self.pid} return SIGINT')
            print()

    def execute_process(self):
        '''
        execute_process(self)

        executa uma instrução do processo e exibe o resultado no terminal
        '''

        self.executed += 1

        if self.executed == self.time:
            self.done = True

        msg = f'P{self.pid} instruction {self.executed}'
        msg += f' of {self.time}' if self.log > 0 else ''
        print(msg)

    def print_process(self):
        '''
        print_process(self)

        exibe informações do processo no terminal
        '''

        print(f'DISPATCHER => P{self.pid}')

        if self.log > 0:
            print(f'       PID     : {self.pid}')
            print(f'       Offset  : {self.offset}')
            print(f'       Blocks  : {self.blocks}')
            print(f'       Priority: {self.priority}')
            print(f'       Time    : {self.time}')
            msg = f'       Printer : 1-{bool(self.devices&pow(2,0))}'
            msg += f'   2-{bool(self.devices&pow(2,1))}'
            print(msg)
            print(f'       Scanner : 1-{bool(self.devices&pow(2,2))}')
            print(f'       Modem   : 1-{bool(self.devices&pow(2,3))}')
            msg = f'       Drives  : 1-{bool(self.devices&pow(2,4))}'
            msg += f'   2-{bool(self.devices&pow(2,5))}'
            print(msg)

        print()

    def queue_operation(self, operation):
        '''
        queue_operation(self, operation)

        adiciona uma operação de arquivo à fila de operações do processo
        '''

        self.operations.append(operation)

    def execute_operation(self, file_manager):
        '''
        execute_operation(self, file_manager)

        executa uma operação de arquivo e exibe seu resultado no terminal
        '''

        if self.operations:
            operation = self.operations.pop(0)

            result = False
            if operation[2]:
                result = file_manager.delete_file(operation[3], self)
            else:
                result = file_manager.write_file(operation[3], operation[4], self.pid)

            msg = f'F{operation[0]} operation '
            msg += 'SUCCESS' if result else 'FAILURE'
            print(msg)

    def print_operation(self, operation):
        '''
        print_operation(self, operation)

        exibe informações basicas de uma operação de arquivo no terminal
        '''

        print(f'OPERATION {operation[0]} =>')

        if self.log > 1:
            mode = 'Delete' if bool(operation[2]) else 'Write'
            print(f'       OID     : {operation[0]}')
            print(f'       User    : {operation[1]}')
            print(f'       Mode    : {mode}')
            print(f'       File    : {operation[3]}')
            print(f'       Size    : {operation[4]} blocks')

    def print_operations(self):
        '''
        print_operations(self)

        executa print_operation(operation) para cada operação de arquivo
        na fila de operações do processo
        '''

        if self.operations:
            for operation in self.operations:
                self.print_operation(operation)
