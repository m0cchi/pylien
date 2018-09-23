import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../../')

from pylien import model
from pylien.parser import lexical

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

l = lexical.FileLexicalAnalyzer(BASE_DIR+'/test.txt')
l.init()
for unit in l.parse():
    if unit.ltype == model.AtomicType.EOF:
        break
    print(unit)

l.destroy()
