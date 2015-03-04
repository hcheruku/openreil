import sys, os, unittest

file_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
reil_dir = os.path.abspath(os.path.join(file_dir, '..'))
if not reil_dir in sys.path: sys.path.append(reil_dir)

from pyopenreil.REIL import *
from pyopenreil.VM import *

from pyopenreil.arch import x86
from pyopenreil.utils import bin_PE

class TestFib(unittest.TestCase):

    BIN_PATH = os.path.join(file_dir, 'fib.exe')

    def test(self):        
    
        addr = 0x004016B0
        reader = bin_PE.Reader(self.BIN_PATH)
        tr = CodeStorageTranslator('x86', reader)

        dfg = DFGraphBuilder(tr).traverse(addr)  
        insn_before = tr.size()

        dfg.eliminate_dead_code()
        dfg.constant_folding()

        dfg.store(tr.storage)
        insn_after = tr.size()

        print tr.storage

        print '%d instructions before optimization and %d after\n' % \
              (insn_before, insn_after)

        cpu = Cpu('x86')
        abi = Abi(cpu, tr)

        testval = 11

        # int fib(int n);
        ret = abi.cdecl(addr, testval)
        cpu.dump()

        print '%d number in Fibonacci sequence is %d' % (testval + 1, ret)    

        assert ret == 144


if __name__ == '__main__':    

    suite = unittest.TestSuite([ TestFib('test') ])
    unittest.TextTestRunner(verbosity = 2).run(suite)

#
# EoF
#
