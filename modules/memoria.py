class MemoryManager:
    def __init__(self, memory, reserved, log):
        self.memory = '0'*memory
        self.queue = []

        self.reserved = reserved
        self.free = memory

        self.log = log

    def __repr__(self):
        return f'[{self.memory[:self.reserved]}][{self.memory[self.reserved:]}]'

    def alloc_mem(self, process):
        if process.offset >= 0:
            return process.offset

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
                print(f'[WARN] MemoryManager: not enough memory.')
                print(f'       P{process.pid} could not find {process.blocks} contiguous blocks.')
                print(f'       Process sleeping now.')
                print()

            self.queue.append(process)
            return -1

        if process.blocks > len(self.memory):
            process.kill = True

            if self.log > 1:
                print(f'[ERROR] MemoryManager: not enough memory.')
                print(f'        P{process.pid} needs {process.blocks} blocks, the system can only ever offer {len(self.memory)}.')
                print(f'        Killing process now.')
                print()

            return -1

        if self.log > 2:
            print(f'[WARN] MemoryManager: not enough memory.')
            print(f'       P{process.pid} requested {process.blocks} blocks, only {self.free} left.')
            print(f'       Process sleeping now.')
            print()

        self.queue.append(process)
        return -1

    def free_mem(self, process):
        if self.queue.count(process):
            self.queue.remove(process)
        else:
            self.memory = self.memory[:process.offset] + '0'*process.blocks + self.memory[process.offset+process.blocks:]
            self.free += process.blocks

        if process.offset > 0:

            transfer = []
            for proc in self.queue:
                if proc.blocks <= self.free:
                    proc.dormant = False
                    transfer.append(proc)

            for proc in transfer:
                self.queue.remove(proc)
