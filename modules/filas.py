class Scheduler:
    def __init__(self, slices, log):
        self.queues = [[] for x in range(len(slices))]
        self.slices = slices

        self.quantum = 0
        self.start = True

        self.log = log

    def __repr__(self):
        return f'{self.queues}'

    #enfileira um processo na fila de processos
    def enqueue_process(self, process):
        if len(self.queues[process.priority]) < 1000:
            self.queues[process.priority].append(process)

            return True

        return False
    
    #tira um processo da fila de processos
    def dequeue_process(self, queue):
        self.start = True
        return self.queues[queue].pop(0)
    
    #tira o processo da fila e coloca de vola com uma prioridade diferente
    def requeue_process(self, src, dst):
        self.start = True
        process = self.dequeue_process(src)
        process.priority = dst
        self.enqueue_process(process)

    #executa os processos das filas, se um processo for muito grande, a prioridade dele diminui e vai sendo refilado
    def execute_processes(self, incoming, memory_manager, device_manager, file_manager):
        for count, queue in enumerate(self.queues):
            if queue:
                if self.start:
                    print(f'PROCESS {queue[0].pid} =>')
                    msg = f'P{queue[0].pid} '
                    msg += 'STARTED' if not queue[0].executed else 'RESTARTED'
                    print(msg)
                    self.start = False

                executed = queue[0].execute_process()
                if file_manager.mode == 'synchronous':
                    if queue[0].operations:
                        queue[0].print_operation(queue[0].operations[0])
                        queue[0].execute_operation(file_manager)

                if self.slices[count] > 0:
                    self.quantum += 1

                if queue[0].done:
                    if self.slices[count] > 0:
                        self.quantum = 0

                    if queue[0].operations:
                        if file_manager.mode == 'synchronous':
                            if self.log > 2:
                                print(f'[WARN] FilesystemManager: file operations pending.')
                                print(f'       P{queue[0].pid} ended without completing {len(queue[0].operations)} file operations in its queue.')

                        elif file_manager.mode == 'batch':
                            queue[0].print_operations()

                            while queue[0].operations:
                                queue[0].execute_operation(file_manager)

                    self.dequeue_process(count).free_resources(memory_manager, device_manager)

                if self.quantum == self.slices[count]:
                    self.requeue_process(count, count + 1 if count<len(self.queues)-1 else 0)
                    self.quantum = 0
                    print()

                return True

        if incoming:
            return True

        return False