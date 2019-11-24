import pyvm.asm

fibonacci = '''
; locations annotated with [..] e.g. [1000] are memory locations.
; variables can be indicated with $var
; labels can be defined with @label on a new line
; to use a memory address in a register of memory location itself
; reference to it with *A or *[1000] OR &A &[1000].

; rename the register to eax, ebx, ecx and edx?
; or name the ra, rb, rc, rd

$a 1              ; set variable a to 1
$b 1              ; set variable b to 1
$max_iter 4       ; set the max iterations
$out_addr 100     ; memory address where to store fibs
mov A 100         ; set $out_address on address 100 to 100
mov [$out_addr] A ; store the out address
mov A $a          ; set a = 1
mov B $b          ; set b = 1
mov D 0           ; set d = 0 (iteration counter)
mov C $max_iter   ; up to 4 iterations (max iterations)
@loop             ; set up a label for the loop
lt D C            ; check D < C
add D 1           ; increment loop counter
jz @end           ; goto end 
mov C B           ; put the value of B in C 
add C A           ; add the value of A to c
mov A B           ; put the value of B in A
mov B C           ; put the value of C in B
mov C [$out_addr] ; load the out address
add C 1           ; increment it
mov [$out_addr] C ; store the new out address
mov *C A          ; store register a in the memory address hold in C
jmp @loop         ; goto address 9
@end              ; set up a label for the end
halt              ; end of program
'''


assembler = pyvm.asm.PyAsm()
assembler.assemble(fibonacci, 'fib.rom')
