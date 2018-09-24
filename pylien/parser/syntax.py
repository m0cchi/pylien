from pylien.model import AtomicType, Unit

class SyntaxAnalyzer(Exception):
    pass

class SyntaxAnalyzer(object):
    def __init__(self, lexical_analyzer):
        self.lexical_analyzer = lexical_analyzer


    def parse_list(self):
        value = []
        for unit in self.lexical_analyzer.parse():
            if unit.ltype == AtomicType.RP:
                break
            elif unit.ltype == AtomicType.LP:
                s = SyntaxAnalyzer(self.lexical_analyzer)
                value.append(s.parse_list())
            elif unit.ltype in [AtomicType.QUOTE, AtomicType.QUASI_QUOTE]:
                quote_value = next(self.parse())
                if quote_value.ltype == AtomicType.EOF:
                    raise SyntaxException()
                unit.value = quote_value
                value.append(unit)
            elif unit.ltype == AtomicType.EOF:
                raise SyntaxException()
            else:
                value.append(unit)
        return Unit(AtomicType.LIST, value)


    def parse(self):
        for unit in self.lexical_analyzer.parse():
            if unit.ltype == AtomicType.EOF:
                break
            if unit.ltype == AtomicType.LP:
                yield self.parse_list()
            elif unit.ltype in [AtomicType.QUOTE, AtomicType.QUASI_QUOTE]:
                quote_value = next(self.parse())
                if quote_value.ltype == AtomicType.EOF:
                    raise SyntaxException()
                unit.value = quote_value
                yield unit
            elif unit.ltype in [AtomicType.SYMBOL, AtomicType.NUMBER, AtomicType.LETTER]:
                pass
        return Unit(AtomicType.EOF)
