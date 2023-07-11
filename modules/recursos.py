class DeviceManager:
	devices = []

	log = 0

	def __init__(self, devices, log):
		for device in devices:
			self.devices.append([device, []])
			self.log = log

	def __repr__(self):
		return f'{self.devices}'

	def in_queue(self, process, did):
		for count, place in enumerate(self.devices[did][1]):
			if process == place:
				return count

		return -1

	def enqueue_device(self, process, did):
		i = self.in_queue(process, did)

		if i < 0:
			self.devices[did][1].append(process)
			return len(self.devices[did][1])-1

		return i

	def dequeue_device(self, process, did):
		if self.devices[did][1].count(process):
			self.devices[did][1].remove(process)

		if self.devices[did][1]:
			self.devices[did][1][0].dormant = False

	def reserve_devices(self, process):
		reserved = True

		if process.devices > pow(2,len(self.devices)-1):
			process.kill = True

			if self.log > 1:
				print()
				print(f'[ERROR] DeviceManager: P{process.pid} requested device not registered in this system.')
				print(f'        Killing Process now.')

			return False

		for did, device in enumerate(self.devices):
			if process.devices&pow(2,did):
				if self.enqueue_device(process, did) != 0:
					reserved = False

					if self.log > 2:
						print(f'[WARN] DeviceManager: P{process.pid} requested device {self.devices[did][0]} already in use.')

		return reserved

	def release_devices(self, process):
		for did, device in enumerate(self.devices):
			if process.devices&pow(2,did):
				self.dequeue_device(process, did)
