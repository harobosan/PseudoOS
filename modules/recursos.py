#devices= lista de dispositivos
#log= informacoes
class DeviceManager:
    def __init__(self, devices, log):
        self.devices = []

        self.log = log

        for device in devices:
            self.devices.append([device, []])

    def __repr__(self):
        return f'{self.devices}'

    #retorna os dispositivos procurados na lista
    def in_queue(self, process, did):
        for count, place in enumerate(self.devices[did][1]):
            if process == place:
                return count

        return -1

    #coloca um dispositivo na lista
    def enqueue_device(self, process, did):
        i = self.in_queue(process, did)

        if i < 0:
            self.devices[did][1].append(process)
            return len(self.devices[did][1])-1

        return i

    #remove um dispositivo da lista
    def dequeue_device(self, process, did):
        if self.devices[did][1].count(process):
            self.devices[did][1].remove(process)

        if self.devices[did][1]:
            self.devices[did][1][0].dormant = False

    #reserva um dispositivo para um processo
    def reserve_devices(self, process):
        reserved = True

        if process.devices > pow(2,len(self.devices)-1):
            process.kill = True

            if self.log > 1:
                print(f'[ERROR] DeviceManager: unknown device.')
                print(f'        P{process.pid} requested a device not registered in this system.')
                print(f'        Killing Process now.')
                print()

            return False

        for did, _ in enumerate(self.devices):
            if process.devices&pow(2,did):
                if self.enqueue_device(process, did) != 0:
                    reserved = False

                    if self.log > 2:
                        print(f'[WARN] DeviceManager: device already in use.')
                        print(f'       P{process.pid} requested busy device {self.devices[did][0]}.')
                        print(f'       Process sleeping now.')
                        print()

        return reserved

    #libera um dispositivo da lista
    def release_devices(self, process):
        for did, _ in enumerate(self.devices):
            if process.devices&pow(2,did):
                self.dequeue_device(process, did)
