class FilesystemManager:
    def __init__(self, storage, mode, log):
        self.storage = '0'*storage
        self.superblock = []

        self.mode = mode
        self.free = storage

        self.log = log

    def __repr__(self):
        return f'[{self.storage}]'

    def set_file(self, name, offset, blocks):
        if offset+blocks <= len(self.storage):
            self.storage = self.storage[:offset] + name*blocks + self.storage[offset+blocks:]
            self.superblock.append([name, offset, blocks, -1])

    def write_file(self, name, blocks, pid):
        for metadata in self.superblock:
            if metadata[0] == name:
                if self.log > 2:
                    print(f'[WARN] FilesystemManager: file already exists.')
                    print(f'       P{pid} failed to create file {name} as it already exists on disk.')

                return False

        if blocks <= self.free:
            segment = self.storage.split('0'*blocks, 1)

            if len(segment) == 2:
                self.storage = segment[0] + name*blocks + segment[1]
                self.free -= blocks
                self.superblock.append([name, len(segment[0]), blocks, pid])

                if self.log > 3:
                    print(f'[INFO] FilesystemManager: file created successfully.')
                    msg = f'       P{pid} created file {name} (block'
                    msg += f's {len(segment[0])}-{len(segment[0])+blocks-1})' if blocks > 1 else f' {len(segment[0])})'
                    print(msg)

                return True

        if self.log > 2:
            print(f'[WARN] FilesystemManager: not enough disk available.')
            print(f'       P{pid} failed to allocate {blocks} blocks for file {name}.')

        return False

    def delete_file(self, name, owner):
        for metadata in self.superblock:
            if metadata[0] == name:
                if owner.priority:
                    if  owner.pid != metadata[2]:
                        if self.log > 2:
                            print(f'[WARN] FilesystemManager: permission denied.')
                            print(f'       P{owner.pid} has no permission to manage file {name}.')

                        return False

                self.storage = self.storage[:metadata[1]] + '0'*metadata[2] + self.storage[metadata[1]+metadata[2]:]
                self.free -= metadata[2]
                self.superblock.remove(metadata)

                if self.log > 3:
                    print(f'[INFO] FilesystemManager: file deleted successfully.')
                    print(f'       P{owner.pid} removed file {name} from the disk.')

                return True

        if self.log > 2:
            print(f'[WARN] FilesystemManager: file not found.')
            print(f'       P{owner.pid} could not delete file {name} as it does not exist.')

        return False
