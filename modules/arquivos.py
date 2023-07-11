class FilesystemManager:
	storage = ''
	free = 0
	superblock = []

	log = 0

	def __init__(self, storage, log):
		self.storage = '0'*storage
		self.free = storage
		self.log = log

	def __repr__(self):
		return f'{self.storage}'

	def write_file(self, name, blocks):
		if blocks <= self.free:
			segment = self.storage.split('0'*blocks, 1)

			if len(segment) == 2:
				self.storage = segment[0] + name*blocks + segment[1]
				self.free -= blocks
				return len(segment[0])

			if self.log > 2:
				print(f'[WARN] FilesystemManager: Pn requested {blocks} blocks, not enough contiguous block were found.')

			return -1

		if blocks > len(self.storage):
			#process.kill = True

			if self.log > 1:
				print()
				print(f'[ERROR] FilesystemManager: Pn requested {blocks} blocks, not enough storage in this system.')
				print(f'        Killing Process now.')

			return -1

	def delete_file(self, name, owner):
		for metadata in self.superblock:
			if metadata[0] == name:
				self.storage = self.storage[:metadata[1]] + '0'*metadata[2] + self.storage[metadata[1]+metadata[2]:]
				self.free -= metadata[2]
				self.superblock.remove(metadata)
				break

	def meta_file(self, name, blocks, owner):
		for metadata in self.superblock:
			if metadata[0] == name:
				if self.log > 1:
					print()
					print(f'[ERROR] already exists')

				return

		offset = self.write_file(name, blocks)

		if offset > 0:
			self.superblock.append([name, offset, blocks, owner])
