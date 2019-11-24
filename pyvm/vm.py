REG_A = 0x00
REG_B = 0x01
REG_C = 0x02
REG_D = 0x03

class PyVM:

    A = 0x00
    B = 0x00
    C = 0x00
    D = 0x00

    IP = 0x00
    ZF = False
    HF = True

    def __init__(self, mem_size):
        self.memory = [0x00] * mem_size

        self.instructions = {
            0x00: self.opcode_nop,
            0x10: self.opcode_halt,
            0x11: self.opcode_jz,
            0x12: self.opcode_jnz,
            0x13: self.opcode_jmp,
            0x81: self.opcode_mov_reg_value,
            0x82: self.opcode_add_reg_reg,
            0x83: self.opcode_sub_reg_reg,
            0x84: self.opcode_mul_reg_reg,
            0x85: self.opcode_eq_reg_reg,
            0x86: self.opcode_gt_reg_reg,
            0x87: self.opcode_lt_reg_reg,
            0x88: self.opcode_add_reg_value,
            0x89: self.opcode_mov_reg_reg,
        }

    def load_rom(self, rom, start_address=0x00):
        rom_size = len(rom)
        if len(self.memory[start_address:]) < rom_size:
            raise Exception('Insufficient memory to load rom.')
        self.memory[start_address:start_address+rom_size] = rom

    def run(self):
        self.HF = False
        while not self.HF:
            self.execute_next_instruction()

    def execute_next_instruction(self):
        instr = self.memory[self.IP]
        # print(self.instructions[instr])
        print('IP: {:04x} Instruction: {:8b}'.format(self.IP, instr))

        if instr & 0x80:
            # two parameter instr
            p1, p2 = self.memory[self.IP+1:self.IP+3]
            self.instructions[instr](p1, p2)
            self.IP += 3
        else:
            # one parameter instr
            p1 = self.memory[self.IP+1]
            self.instructions[instr](p1)
            self.IP += 2

    def read_register(self, reg):
        if reg == REG_A: return self.A
        elif reg == REG_B: return self.B
        elif reg == REG_C: return self.C
        elif reg == REG_D: return self.D
        else:
            raise Exception('Invalid register {}'.format(reg))

    def write_register(self, reg, value):
        self.check_overflow(value)
        if reg == REG_A: self.A = value
        elif reg == REG_B: self.B = value
        elif reg == REG_C: self.C = value
        elif reg == REG_D: self.D = value
        else:
            raise Exception('Invalid register {}'.format(reg))

    def opcode_add_reg_reg(self, r1, r2):
        v1 = self.read_register(r1)
        v2 = self.read_register(r2)
        self.check_overflow(v1 + v2)
        self.write_register(r1, v1 + v2)

    def opcode_add_reg_value(self, r1, value):
        v = self.read_register(r1)
        self.check_overflow(v + value)
        self.write_register(r1, v + value)

    def opcode_sub_reg_reg(self, r1, r2):
        v1 = self.read_register(r1)
        v2 = self.read_register(r2)
        self.write_register(r1, v1 - v2)

    def opcode_mul_reg_reg(self, r1, r2):
        v1 = self.read_register(r1)
        v2 = self.read_register(r2)
        self.check_overflow(v1 * v2)
        self.write_register(r1, v1 * v2)

    def opcode_mov_reg_value(self, reg, value):
        self.check_overflow(value)
        self.write_register(reg, value)

    def opcode_mov_reg_reg(self, r1, r2):
        v = self.read_register(r2)
        self.write_register(r1, v)

    def opcode_eq_reg_reg(self, r1, r2):
        r1 = self.read_register(r1)
        r2 = self.read_register(r2)
        self.ZF = r1 == r2

    def opcode_gt_reg_reg(self, r1, r2):
        r1 = self.read_register(r1)
        r2 = self.read_register(r2)
        self.ZF = r1 > r2

    def opcode_lt_reg_reg(self, r1, r2):
        r1 = self.read_register(r1)
        r2 = self.read_register(r2)
        self.ZF = r1 < r2

    def opcode_jz(self, address):
        if not self.ZF:
            self.IP = address - 2

    def opcode_jnz(self, address):
        if self.ZF:
            self.IP = address - 2

    def opcode_jmp(self, address):
        self.IP = address - 2

    def check_overflow(self, value):
        if not 0 <= value < 2**16:
            raise Exception('Overflow.')

    def opcode_halt(self, _):
        self.HF = True

    def opcode_nop(self, _):
        pass

    def print_state(self):
        print('[State] A={:04x}, B={:04x}, C={:04x}, D={:04x}, IP={:04x}, ZF={}, HF={}'.format(
            self.A,
            self.B,
            self.C,
            self.D,
            self.IP,
            self.ZF,
            self.HF
        ))
