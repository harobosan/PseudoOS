memory = '0' * 1024

def alloc_mem(blocks, user):
	global memory

	if not user:
		seg = memory.split('0' * blocks,1)

	else:
		seg = memory[64:].split('0' * blocks,1)
		seg[0] = memory[:64]+seg[0]

	if len(seg) == 2:
		memory = seg[0] + '1' * blocks + seg[1]
		return len(seg[0])

	return -1

def free_mem(blocks, offset):
	global memory

	memory = memory[:offset] + '0' * blocks + memory[offset+blocks:]

def print_mem():
	print(memory)
