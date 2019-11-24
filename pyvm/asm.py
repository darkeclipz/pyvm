class PyAsm:

    registers = ['A', 'B', 'C', 'D']

    def __init__(self):
        pass

    def remove_comments(self, line):
        if ';' in line:
            line = line[:line.index(';')]
        return line

    def parse_instruction(self, instruction):

        n = len(instruction)
        if n == 1:
            return self.parse_single(instruction[0])
        elif n == 2:
            return self.parse_double(instruction[0], instruction[1])
        elif n == 3:
            return self.parse_multiple(instruction[0], instruction[1], instruction[2])
        else:
            raise Exception('Invalid instruction {}'.format(instruction))

    def parse_single(self, opcode):
        if opcode == 'NOP': return [0x00]
        elif opcode == 'HALT': return [0x10]
        else:
            raise Exception('Invalid opcode {}'.format(opcode))

    def parse_double(self, opcode, arg):
        arg = int(arg)
        if opcode == 'JZ': return [0x11, arg]
        elif opcode == 'JNZ': return [0x12, arg]
        elif opcode == 'JMP': return [0x13, arg]
        else:
            raise Exception('Invalid opcode {}'.format(opcode))

    def cast_to_register(self, arg):
        if arg == 'A': return 0x00
        elif arg == 'B': return 0x01
        elif arg == 'C': return 0x02
        elif arg == 'D': return 0x03
        else:
            raise Exception('Invalid register to cast {}'.format(arg))

    def parse_multiple(self, opcode, arg1, arg2):
        if opcode == 'MOV' and arg2 not in self.registers:
            return [0x81, self.cast_to_register(arg1), int(arg2)]
        elif opcode == 'MOV' and arg2 in self.registers:
            return [0x89, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'ADD' and arg2 in self.registers:
            return [0x82, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'ADD' and arg2 not in self.registers:
            return [0x88, self.cast_to_register(arg1), int(arg2)]
        elif opcode == 'SUB':
            return [0x83, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'MUL':
            return [0x84, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'EQ':
            return [0x85, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'GT':
            return [0x86, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        elif opcode == 'LT':
            return [0x87, self.cast_to_register(arg1), self.cast_to_register(arg2)]
        else:
            raise Exception('Invalid opcode {}'.format(opcode))

    def assemble(self, asm, file_out):
        with open(file_out, 'wb') as f:
            for i, line in enumerate(asm.split('\n')):
                line = self.remove_comments(line)
                line = line.strip()
                if len(line) == 0:
                    continue
                line = line.upper()
                instruction = line.split(' ')
                data = bytearray(self.parse_instruction(instruction))
                f.write(data)
                print('{}: {} ({})'.format(i, line, instruction))
                print('data: {}'.format(data))
