from pylien.model import Function, Unit, AtomicType, env

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
        
env.set_function('print', Unit(AtomicType.FUNCTION, PrintFn()))
