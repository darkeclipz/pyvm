import pyvm.asm

example = '''
; instructions
nop
jz 0
jnz 0
jmp 0
mov A 1
add A B
sub A B
mul A B
eq A B
gt A B
lt A B
add A 1
halt
'''


assembler = pyvm.asm.PyAsm()
assembler.assemble(example, 'example.rom')
