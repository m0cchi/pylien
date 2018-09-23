import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from pylien import model
from pylien.parser import lexical, syntax

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

l = lexical.FileLexicalAnalyzer(BASE_DIR + '/test.txt')
l.init()

s = syntax.SyntaxAnalyzer(l)
for unit in s.parse():
    if unit.ltype == model.AtomicType.EOF:
        break
    print(unit)

l.destroy()
