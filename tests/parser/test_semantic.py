import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from pylien import model
from pylien.parser import lexical, syntax, semantic
from pylien import built_in

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

l = lexical.FileLexicalAnalyzer(BASE_DIR + '/test2.txt')
l.init()

s = syntax.SyntaxAnalyzer(l)
p = semantic.SemanticAnalyzer(model.env)

for unit in s.parse():
    if unit.ltype == model.AtomicType.EOF:
        break
    u = p.eval(unit)
    print(u)

l.destroy()
