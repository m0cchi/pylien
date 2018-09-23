from pylien.model import Unit, AtomicType

class ParseException(Exception):
    pass

class LexicalAnalyzer(object):
    SKIP = ('\n', '\r', '\t', ' ',)
    COMMENT = ';'
    NUMBERS = tuple('1234567890')

    def init(self):
        self.stack = []

    def destroy(self):
        pass

    def set_rs(self, rs):
        self.rs = rs

    def push(self, ch):
        self.stack.append(ch)

    def pop(self):
        return self.stack.pop()

    def parse_letter(self):
        value = []
        while True:
            ch = self.read()

            if len(ch) == 0:
                raise ParseException()
            elif ch != '"':
                value.append(ch)
            else:
                break
        return ''.join(value)

    def parse_number(self):
        value = []
        dot_count = 0 
        while True:
            ch = self.read()

            if len(ch) == 0:
                break

            if ch == '.':
                if dot_count > 0:
                    raise ParseException()
                dot_count += 1
                value.append(ch)
            elif ch in LexicalAnalyzer.NUMBERS:
                value.append(ch)
            else:
                self.unread(ch)
                break
        return ''.join(value)

    def parse_symbol(self):
        value = []
        while True:
            ch = self.read()

            if len(ch) == 0:
                break
            if ch in LexicalAnalyzer.SKIP:
                break
            if ch in ['(', ')', ',']:
                self.unread(ch)
                break
            value.append(ch)
        return ''.join(value)

    def read(self):
        return self.pop() if len(self.stack) > 0 else self.rs.read(1)

    def unread(self, ch):
        self.push(ch)

    def parse(self):
        while True:
            ch = self.read()
            if len(ch) == 0:
                yield Unit(AtomicType.EOF)
            if ch == LexicalAnalyzer.COMMENT:
                while True:
                    ch = self.read(1)
                    if len(ch) == 0:
                        return Unit(AtomicType.EOF)
                    if ch == '\n':
                        break

            if ch == '(':
                yield Unit(AtomicType.LP)
            elif ch == ')':
                yield Unit(AtomicType.RP)
            elif ch == '"':
                yield Unit(AtomicType.LETTER, self.parse_letter())
            elif ch in LexicalAnalyzer.NUMBERS:
                self.unread(ch)
                yield Unit(AtomicType.NUMBER, self.parse_number())
            elif ch == "'":
                yield Unit(AtomicType.QUOTE)
            elif ch == "`":
                yield Unit(AtomicType.QUASI_QUOTE)
            elif ch == ",":
                yield Unit(AtomicType.COMMA)
            elif ch in LexicalAnalyzer.SKIP:
                continue
            else:
                self.unread(ch)
                ret = self.parse_symbol()
                if ret == 'T':
                    yield Unit(AtomicType.BOOL, True)
                elif ret == 'nil':
                    yield Unit(AtomicType.NIL, None)
                else:
                    yield Unit(AtomicType.SYMBOL, ret)


class FileLexicalAnalyzer(LexicalAnalyzer):

    def __init__(self, filepath):
        self.filepath = filepath


    def init(self):
        super(FileLexicalAnalyzer, self).init()

        self.rs = open(self.filepath, 'r')
        super(FileLexicalAnalyzer, self).set_rs(self.rs)

    def destroy(self):
        self.rs.close()

