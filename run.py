import pyvm.vm
import pyvm.helpers

vm = pyvm.vm.PyVM(mem_size=128)
rom = pyvm.helpers.read_bytes_from_file('fib.rom')
vm.load_rom(rom)
pyvm.helpers.dump_mem(vm.memory, n_size=8)
vm.run()
vm.print_state()
