class FilesystemManager:
    '''
    Gerenciador de Sistema de Arquivos

    storage= string representando blocos de disco
    superblock= lista de metadados de arquivos
    mode= string de modo de operação
    free= quantidade de blocos de disco livres
    log= nível de verbose
    '''

    def __init__(self, storage, mode, log):
        self.storage = '0'*storage
        self.superblock = []

        self.mode = mode
        self.free = storage

        self.log = log

    def __repr__(self):
        return f'[{self.storage}]'

    def set_file(self, name, offset, blocks):
        '''
        set_file(self, name, offset, blocks)

        escreve um arquivo de nome 'name' diretamente no disco
        na posição 'offset' em uma quantidade 'blocks' de blocos
        '''

        if offset+blocks <= len(self.storage):
            self.storage = self.storage[:offset] + name*blocks + self.storage[offset+blocks:]
            self.superblock.append([name, offset, blocks, -1])

    def write_file(self, name, blocks, pid):
        '''
        write_file(self, name, blocks, pid)

        escreve um arquivo em disco de nome 'name' com 'blocks' blocs de comprimento
        caso encontre espaço suficiente, guarda os metadados em superblock

        retorna: bool se a operação conseguiu escrever o arquivo
        '''

        for metadata in self.superblock:
            if metadata[0] == name:
                if self.log > 2:
                    print('[WARN] FilesystemManager: file already exists.')
                    msg = f'       P{pid} failed to create file'
                    msg += f' {name} as it already exists on disk.'
                    print(msg)

                return False

        if blocks <= self.free:
            segment = self.storage.split('0'*blocks, 1)

            if len(segment) == 2:
                self.storage = segment[0] + name*blocks + segment[1]
                self.free -= blocks
                self.superblock.append([name, len(segment[0]), blocks, pid])

                if self.log > 3:
                    print('[INFO] FilesystemManager: file created successfully.')
                    msg = f'       P{pid} created file {name} (block'
                    msg_1 = f's {len(segment[0])}-{len(segment[0])+blocks-1})'
                    msg_2 = f' {len(segment[0])})'
                    msg += msg_1 if blocks > 1 else msg_2
                    print(msg)

                return True

        if self.log > 2:
            print('[WARN] FilesystemManager: not enough disk available.')
            print(f'       P{pid} failed to allocate {blocks} blocks for file {name}.')

        return False

    def delete_file(self, name, owner):
        '''
        delete_file(self, name, owner)

        libera o espaço de disco ocupado por um arquivo de nome 'name'
        se 'owner' tiver permissão para fazê-lo

        retorna: bool se a operação conseguiu deletar o arquivo
        '''

        for metadata in self.superblock:
            if metadata[0] == name:
                if owner.priority:
                    if  owner.pid != metadata[2]:
                        if self.log > 2:
                            print('[WARN] FilesystemManager: permission denied.')
                            print(f'       P{owner.pid} has no permission to manage file {name}.')

                        return False

                pre = self.storage[:metadata[1]]
                pos = self.storage[metadata[1]+metadata[2]:]
                self.storage = pre + '0'*metadata[2] + pos
                self.free -= metadata[2]
                self.superblock.remove(metadata)

                if self.log > 3:
                    print('[INFO] FilesystemManager: file deleted successfully.')
                    print(f'       P{owner.pid} removed file {name} from the disk.')

                return True

        if self.log > 2:
            print('[WARN] FilesystemManager: file not found.')
            print(f'       P{owner.pid} could not delete file {name} as it does not exist.')

        return False
