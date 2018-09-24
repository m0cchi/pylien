from pylien.model import Function, Macro, Unit, AtomicType, env

class PrintFn(Function):
    def __init__(self):
        super(PrintFn, self).set_args([Function.REST, 'args'])

    def call(self, env, body):
        env = super(PrintFn, self).parse_args(env, body)
        import sys
        args = env.get_variable('args')
        for arg in args.value:
            sys.stdout.write(str(arg.value))
        sys.stdout.flush()
        print()
        return Unit(AtomicType.NIL)

class DefvarMc(Macro):
    def __init__(self):
        super(DefvarMc, self).set_args(['defvar name', 'defvar value'])

    def call(self, env, body):
        env = super(DefvarMc, self).parse_args(env, body)
        name = env.get_variable(self.args[0])
        value = env.get_variable(self.args[1])

        from pylien.parser.semantic import SemanticAnalyzer
        s = SemanticAnalyzer(env.parent)

        env.parent.set_variable(name.value, s.eval(value))
        return Unit(AtomicType.NIL)


env.set_function('print', Unit(AtomicType.FUNCTION, PrintFn()))
env.set_function('defvar', Unit(AtomicType.MACRO, DefvarMc()))
