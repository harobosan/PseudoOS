resources = [[],[],[],[],[],[]]

def in_queue(pid, rid):
	for i in range(len(resources[rid])):
		if pid == resources[rid][i]:
			return i

	return -1

def enqueue_resource(pid, rid):
	i = in_queue(pid, rid)

	if i < 0:
		resources[rid].append(pid)
		return len(resources[rid])-1

	return i

def dequeue_resource(rid):
	resources[rid].pop(0)

def reserve_resources(pid, requested):
	for i in range(6):
		if requested&pow(2,i):
			if enqueue_resource(pid, i) != 0:
				return False

	return True

def release_resources(requested):
	for i in range(6):
		if requested&pow(2,i):
			dequeue_resource(i)

def print_resources():
	print(resources)
