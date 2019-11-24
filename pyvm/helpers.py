#MAGIC_HEADER = [0x69, 0x01, 0x02, 0x069]


def read_bytes_from_file(file_path):
    with open(file_path, 'rb') as f:
        return list(f.read())


def read_lines_from_file(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


def dump_mem(memory, n_size=8, start=0, stop=-1):
    if stop == -1:
        stop = len(memory)
    print('Total memory size: {} bytes / {} kb'.format(len(memory), len(memory) / 1024))
    for i in range(start, stop, n_size):
        buffer = ''
        for j in range(i, i+n_size):
            buffer += ('{:b} '.format(memory[j])).rjust(9, '0')
        buffer += '| '
        for j in range(i, i+n_size):
            buffer += '{:01x}'.format(memory[j]).rjust(2, '0')
            if j & 1:
                buffer += '   '
            else:
                buffer += ' '
        print('{}: {}'.format(str(i).rjust(4, '0'), buffer))
