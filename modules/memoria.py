class MemoryManager:
    '''
    Gerenciador de Memória

    memory= strings representando blocos de memória
            particionados em parte reservada e de
            usuário
    queues= filas de espera de processos
    free= quantidade de blocos de memória livres
    log= nível de verbose
    '''

    def __init__(self, memory, reserved, log):
        self.memory = ['0'*reserved, '0'*(memory-reserved)]
        self.queues = [[], []]

        self.limit = [reserved, memory-reserved]
        self.free = [reserved, memory-reserved]


        self.log = log

    def __repr__(self):
        return f'[{self.memory[0]}][{self.memory[1]}]'

    def alloc_mem(self, process):
        '''
        alloc_mem(self, process)

        aloca blocos de memória contígua para um processo 'process'

        retorna: o offset da memória alocada, -1 em caso de falha
        '''

        if process.offset >= 0:
            return process.offset

        part = int(bool(process.priority))

        if process.blocks > self.limit[part]:
            process.kill = True

            if self.log > 1:
                print('[ERROR] MemoryManager: not enough memory.')
                msg = f'        P{process.pid} needs {process.blocks} blocks,'
                msg += ' the system can only ever offer'
                msg+= f' {self.limit[part]}.'
                print(msg)
                print('        Killing process now.')
                print()

            return -1

        if process.blocks <= self.free[part]:
            segment = self.memory[part].split('0'*process.blocks, 1)

            if len(segment) == 2:
                self.memory[part] = segment[0] + '1'*process.blocks + segment[1]
                self.free[part] -= process.blocks
                offset = len(segment[0]) + (self.limit[0] if part else 0)

                if self.log > 3:
                    print('[INFO] MemoryManager: memory allocated successfully.')
                    msg = f'       P{process.pid} allocated {process.blocks} of memory'
                    msg += ' (block'
                    msg_1 = f's {offset}-{offset+process.blocks-1})'
                    msg_2 = f' {offset})'
                    msg += msg_1 if process.blocks > 1 else msg_2
                    print(msg)
                    print()

                return offset

            if self.log > 2:
                print('[WARN] MemoryManager: not enough memory.')
                print(f'       P{process.pid} could not find {process.blocks} contiguous blocks.')
                print('       Process sleeping now.')
                print()

            self.queues[part].append(process)
            return -1

        if self.log > 2:
            print('[WARN] MemoryManager: not enough memory.')
            msg = f'       P{process.pid} requested {process.blocks} blocks,'
            msg += f' only {self.free[part]} left.'
            print(msg)
            print('       Process sleeping now.')
            print()

        self.queues[part].append(process)
        return -1

    def free_mem(self, process):
        '''
        free_mem(self, process)

        libera os blocos de memória alocados por um processo 'process'
        '''

        part = int(bool(process.priority))

        if self.queues[part].count(process):
            self.queues[part].remove(process)
        else:
            offset = process.offset - (self.limit[0] if part else 0)
            pre = self.memory[part][:offset]
            pos = self.memory[part][offset+process.blocks:]
            self.memory[part] = pre + '0'*process.blocks + pos
            self.free[part] += process.blocks
            process.offset = -1

            transfer = []
            for proc in self.queues[part]:
                if proc.blocks <= self.free[part]:
                    proc.dormant = False
                    transfer.append(proc)

            for proc in transfer:
                self.queues[part].remove(proc)
