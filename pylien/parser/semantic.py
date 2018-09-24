from pylien.model import AtomicType, Unit, Environment

class SemanticAnalyzer(object):

    def __init__(self, env=Environment()):
        self.env = env

    def eval_list(self, unit):
        first = unit.value.pop(0)
        first = self.eval(first)
        func_unit = self.env.get_function(first.value)
        ret = func_unit.value.call(self.env, unit)
        if func_unit.ltype == AtomicType.MACRO:
            self.eval(ret)
        return ret

    def eval(self, unit):
        if unit.ltype == AtomicType.LIST:
            return self.eval_list(unit)
        elif unit.ltype in [AtomicType.QUOTE, AtomicType.QUASI_QUOTE]:
            return unit.value
        else:
            return unit

