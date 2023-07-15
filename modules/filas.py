class Scheduler:
    '''
    Escalonador

    queues= lista de filas de execução
    slices= lista de time slices alocados para cada fila
    quantum= contador de quantum
    mode= modo de contagem do quantum
    start= flag de estado
    log= nível de verbose
    '''

    def __init__(self, slices, mode, log):
        self.queues = [[] for x in slices]
        self.slices = slices

        self.quantum = .0
        self.mode = mode
        self.start = True

        self.log = log

    def __repr__(self):
        return f'{self.queues}'

    def enqueue_process(self, process):
        '''
        enqueue_process(self, process)

        adiciona um processo à fila equivalente à prioridade do processo

        retorno: bool se a fila possui posições restantes para executar o processo
        '''

        if process.priority > len(self.queues)-1:
            process.priority = len(self.queues)-1

        if len(self.queues[process.priority]) < 1000:
            self.queues[process.priority].append(process)

            return True

        return False

    def dequeue_process(self, queue):
        '''
        dequeue_process(self, queue)

        remove um processo da fila de prioridade 'queue'

        retorno: o processo removido da fila
        '''

        self.start = True
        return self.queues[queue].pop(0)

    def requeue_process(self, src, dst):
        '''
        requeue_process(self, src, dst)

        move um processo da fila de prioridade 'src' para a fila de prioridade 'dst'
        '''

        self.start = True
        process = self.dequeue_process(src)
        process.priority = dst
        self.enqueue_process(process)

    def execute_processes(self, delta, incoming, memory_manager, device_manager, file_manager):
        '''
        execute_processes(self, delta_t, incoming, memory_manager, device_manager, file_manager)

        executa um ciclo de CPU

        retorno: bool se ainda há processos a serem executados
        '''

        for count, queue in enumerate(self.queues):
            if queue:
                if self.start:
                    print(f'PROCESS {queue[0].pid} =>')
                    msg = f'P{queue[0].pid} '
                    msg += 'STARTED' if not queue[0].executed else 'RESTARTED'
                    print(msg)
                    self.start = False

                queue[0].execute_process()

                if self.slices[count] > 0:
                    if self.mode == 'cycle':
                        self.quantum += 1
                    else:
                        self.quantum += delta

                        if self.log > 3:
                            print(f'   quantum {round(self.quantum,2)} of {self.slices[count]}')

                if file_manager.mode == 'synchronous':
                    if queue[0].operations:
                        queue[0].execute_operation(file_manager)

                if queue[0].done:
                    if self.slices[count] > 0:
                        self.quantum = 0

                    if queue[0].operations:
                        if file_manager.mode == 'synchronous':
                            if self.log > 2:
                                print('[WARN] FilesystemManager: file operations pending.')
                                msg = f'       P{queue[0].pid} ended without completing'
                                msg += f' {len(queue[0].operations)} file operations in its queue.'
                                print(msg)

                        elif file_manager.mode == 'syncbatch':
                            while queue[0].operations:
                                queue[0].execute_operation(file_manager)

                    self.dequeue_process(count).free_resources(memory_manager, device_manager)

                if self.slices[count] > 0 and self.quantum > self.slices[count]:
                    self.requeue_process(count, count + 1 if count<len(self.queues)-1 else 0)
                    self.quantum = 0
                    print()

                return False

        if incoming:
            return False

        return True
