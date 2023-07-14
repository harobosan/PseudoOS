class DeviceManager:
    '''
    Gerenciador de Dispositivos

    devices= lista de dispositivos e suas filas de espera
    log= nível de verbose
    '''

    def __init__(self, devices, log):
        self.devices = []

        self.log = log

        for device in devices:
            self.devices.append([device, []])

    def __repr__(self):
        return f'{self.devices}'

    def in_queue(self, process, did):
        '''
        in_queue(self, process, did)

        busca um processo 'process' na fila de espera
        de um dispositivo identificado por 'did'

        retorna: a posição de 'process' na fila
        '''

        for count, place in enumerate(self.devices[did][1]):
            if process == place:
                return count

        return -1

    def enqueue_device(self, process, did):
        '''
        enqueue_device(self, process, did)

        adiciona um processo 'process' na fila de espera
        de um dispositivo identificado por 'did'

        retorna: a posição de 'process' na fila de espera
        '''

        i = self.in_queue(process, did)

        if i < 0:
            self.devices[did][1].append(process)
            return len(self.devices[did][1])-1

        return i

    def dequeue_device(self, process, did):
        '''
        dequeue_device(self, process, did)

        remove um processo 'process' da fila de espera
        de um dispositivo identificado por 'did'
        caso se encontre na fila
        '''

        if self.devices[did][1].count(process):
            self.devices[did][1].remove(process)

        if self.devices[did][1]:
            self.devices[did][1][0].dormant = False

    def reserve_devices(self, process):
        '''
        reserve_devices(self, process)

        tenta reservar dispositivos para um processo 'process'

        retorna: bool se os dispositivos conseguiram ser reservados
        '''

        reserved = True

        if process.devices > pow(2,len(self.devices)-1):
            process.kill = True

            if self.log > 1:
                print('[ERROR] DeviceManager: unknown device.')
                print(f'        P{process.pid} requested a device not registered in this system.')
                print('        Killing Process now.')
                print()

            return False

        for did, _ in enumerate(self.devices):
            if process.devices&pow(2,did):
                if self.enqueue_device(process, did) != 0:
                    reserved = False

                    if self.log > 2:
                        print('[WARN] DeviceManager: device already in use.')
                        msg = f'       P{process.pid} requested busy device'
                        msg += f' {self.devices[did][0]}.'
                        print(msg)
                        print('       Process sleeping now.')
                        print()

        return reserved

    def release_devices(self, process):
        '''
        release_devices(self, process)

        libera todos os dispositivos reservados por um processo 'process'
        '''

        for did, _ in enumerate(self.devices):
            if process.devices&pow(2,did):
                self.dequeue_device(process, did)
