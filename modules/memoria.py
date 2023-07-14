class MemoryManager:
    '''
    Gerenciador de Memória

    memory= string representando blocos de memória
    queue= fila de espera de processos
    reserved= quantidade de blocos de memória reservado
              para processos de alta prioridade
    free= quantidade de blocos de memória livres
    log= nível de verbose
    '''

    def __init__(self, memory, reserved, log):
        self.memory = '0'*memory
        self.queue = []

        self.reserved = reserved if reserved < memory else memory
        self.limit = memory
        self.free = memory

        self.log = log

    def __repr__(self):
        return f'[{self.memory[:self.reserved]}][{self.memory[self.reserved:]}]'

    def alloc_mem(self, process):
        '''
        alloc_mem(self, process)

        aloca blocos de memória contígua para um processo 'process'

        retorna: o offset da memória alocada, -1 em caso de falha
        '''

        if process.offset >= 0:
            return process.offset

        if process.blocks > (self.limit-self.reserved if process.priority else self.limit):
            process.kill = True

            if self.log > 1:
                print('[ERROR] MemoryManager: not enough memory.')
                msg = f'        P{process.pid} needs {process.blocks} blocks,'
                msg += ' the system can only ever offer'
                msg+= f' {self.limit-self.reserved if process.priority else self.limit}.'
                print(msg)
                print('        Killing process now.')
                print()

            return -1

        if process.blocks <= self.free:
            if process.priority:
                segment = self.memory[self.reserved:].split('0'*process.blocks, 1)
                segment[0] = self.memory[:self.reserved]+segment[0]
            else:
                segment = self.memory.split('0'*process.blocks, 1)

            if len(segment) == 2:
                self.memory = segment[0] + '1'*process.blocks + segment[1]
                self.free -= process.blocks
                return len(segment[0])

            if self.log > 2:
                print('[WARN] MemoryManager: not enough memory.')
                print(f'       P{process.pid} could not find {process.blocks} contiguous blocks.')
                print('       Process sleeping now.')
                print()

            self.queue.append(process)
            return -1

        if self.log > 2:
            print('[WARN] MemoryManager: not enough memory.')
            msg = f'       P{process.pid} requested {process.blocks} blocks,'
            msg += f' only {self.free} left.'
            print(msg)
            print('       Process sleeping now.')
            print()

        self.queue.append(process)
        return -1

    def free_mem(self, process):
        '''
        free_mem(self, process)

        libera os blocos de memória alocados por um processo 'process'
        '''

        if self.queue.count(process):
            self.queue.remove(process)
        else:
            pre = self.memory[:process.offset]
            pos = self.memory[process.offset+process.blocks:]
            self.memory = pre + '0'*process.blocks + pos
            self.free += process.blocks

        if process.offset > 0:
            transfer = []
            for proc in self.queue:
                if proc.blocks <= self.free:
                    proc.dormant = False
                    transfer.append(proc)

            for proc in transfer:
                self.queue.remove(proc)
