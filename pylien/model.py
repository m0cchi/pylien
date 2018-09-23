from enum import Enum, unique

class NameException(Exception):
    pass

@unique
class AtomicType(Enum):
    def auto():
        count = 0
        while True:
            count += 1
            yield count

    EOF = auto()
    LP = auto()
    RP = auto()
    QUOTE = auto()
    QUASI_QUOTE = auto()
    COMMA = auto()
    NIL = auto()
    LETTER = auto()
    NUMBER = auto()
    BOOL = auto()
    SYMBOL = auto()

    LIST = auto()
    FUNCTION = auto()
    MACRO = auto()

class Unit(object):
    def __init__(self, ltype, value=None):
        self.ltype = ltype
        self.value = value

    def __str__(self):
        if isinstance(self.value, list):
            return '{}: {}'.format(self.ltype, list(map(str, self.value)))
        return '{}: {}'.format(self.ltype, self.value)

class Function(object):
    REST = '&rest'
    def __init__(self):
        self.args = []

    def set_args(self, args):
        self.args = args

    def parse_args(self, env, body):
        from pylien.parser.semantic import SemanticAnalyzer
        s = SemanticAnalyzer(env)

        env = Environment(env)
        args = iter(map(lambda a: s.eval(a), body.value))
        defargs = iter(self.args)
        for arg in defargs:
            if arg == Function.REST:
                v = []
                for a in args:
                    v.append(a)
                env.set_variable(next(defargs), Unit(AtomicType.LIST, v))
            else:
                env.set_variable(arg, next(args))
        return env

class Environment(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}
        self.functions = {}

    def set_variable(self, varname, value):
        self.variables[varname] = value

    def get_variable(self, varname):
        if varname in self.variables:
            return self.variables[varname]
        parent = self.parent
        while parent != None:
            if varname in parent.variables:
                return parent[varname]
        raise NameException()

    def set_function(self, funcname, value):
        self.functions[funcname] = value

    def get_function(self, funcname):
        if funcname in self.functions:
            return self.functions[funcname]
        parent = self.parent
        while parent != None:
            if funcname in parent.functions:
                return parent[funcname]
        raise NameException()
env = Environment()
