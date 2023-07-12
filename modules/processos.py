class Process:
    #pid=id do processo
	#arrival=ordem de chegada
	#prioriry=prioridade do processo
	#time= tempo para complecao do processo
	#executed= quantas vezes o processo foi executado
	#lifetime= tempo de vida do processo
    def __init__(self, pid, arrival, priority, time, blocks, log):
        self.pid = pid
        self.arrival = arrival
        self.priority = priority

        self.time = time
        self.executed = 0
        self.lifetime = 0

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
        self.devices += sata
        self.devices <<= 1
        self.devices += modem
        self.devices <<= 1
        self.devices += scanner
        self.devices <<= 2
        self.devices += printer
        
	#aloca os recursos
    def alloc_resources(self, memory_manager, device_manager):
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

	#libera os recursos
    def free_resources(self, memory_manager, device_manager):
        if self.devices > 0:
            device_manager.release_devices(self)

        if self.offset >= 0:
            memory_manager.free_mem(self)

        if not self.kill:
            print(f'P{self.pid} return SIGINT')
            print()

    def execute_process(self):
        self.executed += 1

        if self.executed == self.time:
            self.done = True

        msg = f'P{self.pid} instruction {self.executed}'
        msg += f' of {self.time}' if self.log > 0 else ''
        print(msg)
        
	#imprime na tela o processo
    def print_process(self):
        print(f'DISPATCHER => P{self.pid}')

        if self.log > 0:
            print(f'       PID     : {self.pid}')
            print(f'       Offset  : {self.offset}')
            print(f'       Blocks  : {self.blocks}')
            print(f'       Priority: {self.priority}')
            print(f'       Time    : {self.time}')
            print(f'       Printer : 1-{bool(self.devices&pow(2,0))}   2-{bool(self.devices&pow(2,1))}')
            print(f'       Scanner : 1-{bool(self.devices&pow(2,2))}')
            print(f'       Modem   : 1-{bool(self.devices&pow(2,3))}')
            print(f'       Drives  : 1-{bool(self.devices&pow(2,4))}   2-{bool(self.devices&pow(2,5))}')

        print()
        
	#coloca a operacao na lista de operacao do processo
    def queue_operation(self, operation):
        self.operations.append(operation)
        
	#executa uma das operacoes do processo
    def execute_operation(self, file_manager):
        if self.operations:
            operation = self.operations.pop(0)

            result = False
            if operation[2]:
                result = file_manager.delete_file(operation[3], self)
            else:
                result = file_manager.write_file(operation[3], operation[4], self.pid)

            msg = f'F{operation[0]} operation '
            msg += f'SUCCESS' if result else f'FAILURE'
            print(msg)

	#imprime uma operacao na tela
    def print_operation(self, operation):
        print(f'OPERATION {operation[0]} =>')

        if self.log > 1:
            mode = 'Delete' if bool(operation[2]) else 'Write'
            print(f'       OID     : {operation[0]}')
            print(f'       User    : {operation[1]}')
            print(f'       Mode    : {mode}')
            print(f'       File    : {operation[3]}')
            print(f'       Size    : {operation[4]} blocks')
	
	#imprime todas as operacoes da fila de operacoes
    def print_operations(self):
        if self.operations:
            for operation in self.operations:
                self.print_operation(operation)
