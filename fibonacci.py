import pyvm.asm

fibonacci = '''
mov A 1  ; set a = 1
mov B 1  ; set b = 1
mov D 0  ; set d = 0 (iteration counter)
mov C 4  ; up to 4 iterations (max iterations)
lt D C   ; check D < C
add D 1  ; increment loop counter
jz 36    ; goto end 
mov C B  ; put the value of B in C 
add C A  ; add the value of A to c
mov A B  ; put the value of B in A
mov B C  ; put the value of C in B
jmp 9    ; goto address 9
nop      ; nop sled....
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
nop
halt     ; EOP
'''


assembler = pyvm.asm.PyAsm()
assembler.assemble(fibonacci, 'fib.rom')
