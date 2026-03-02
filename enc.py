import sys, os, marshal, ast, random, builtins, string
from ast import *
def rb():
    return ''.join(random.choices([chr(i) for i in range(44032, 55204) if chr(i).isprintable() and chr(i).isidentifier()], k=11))

def rb2():
    return ''.join(random.choices([chr(i) for i in range(44032, 55204) if chr(i).isprintable() and chr(i).isidentifier()], k=10))

def encunicode():
    pool = []
    pool += list(range(0x2160, 0x217F))
    pool += list(range(0x2C00, 0x2C5F))
    pool += list(range(0x0180, 0x024F))
    pool += random.sample(range(0xE000, 0xF8FF), 15)

    random.shuffle(pool)
    return [chr(x) for x in pool[:16]]

meo = encunicode()

checkvs = r'''
with open(__file__, "r", encoding="utf-8") as f:
    data = f.read()

expected = f"""if str(__import__('sys').version[0:4]) != '{str(eval("__import__('sys').version[0:4]"))}':
    print('You need to Install Python {str(eval("__import__('sys').version[0:4]"))}')
    __import__("sys").exit()"""

if expected not in data:
    raise __builtins__['Version']
'''

anhambuiltins = checkvs+"""
import sys

_b = sys.modules['builtins']
__p = getattr(_b, ''.join(chr(i) for i in (112,114,105,110,116)))
__e = getattr(_b, ''.join(chr(i) for i in (101,118,97,108)))
__x = getattr(_b, ''.join(chr(i) for i in (101,120,101,99)))
for _n in ('print', 'eval', 'exec'):
    globals().pop(_n, None)

del _b, _n
"""

antihookvip = anhambuiltins+"""
class __ngan_hook_builtins__:
    def __init__(self):
        try:
            self.p = builtins.print
            self.e = builtins.exec
            self.v = builtins.eval
        except:
            self.p = self.e = self.v = None

    def check(self):
        try:
            if self.p and builtins.print != self.p:
                raise fn
            if self.e and builtins.exec != self.e:
                raise fn
            if self.v and builtins.eval != self.v:
                raise fn
        except SystemExit:raise fn
        except:pass
__rt = __ngan_hook_builtins__()
"""

checkcuoi = """
with open(__file__, "r", encoding="utf-8") as f:
    data = ''.join(f.read().split())

if (
    f"exceptExceptionase:print(e)" not in data
):
    raise e

if (
    f"exceptKeyboardInterrupt:pass" not in data
):
        raise Crackconcak
"""

anti = antihookvip+checkcuoi+"""
if str(__import__('sys').exit) != '<built-in function exit>':
    raise fn
if str(print) != '<built-in function print>':
    raise fn
if str(exec) != '<built-in function exec>':
    raise fn
if str(input) != '<built-in function input>':
    raise fn
if str(len) != '<built-in function len>':
    raise fn
if str(__import__('marshal').loads) != '<built-in function loads>':
    raise fn
if 'dis' in globals() and hasattr(dis,'dis') and 'built-in' not in str(dis.dis): raise SystemExit
with open(__file__,'r',encoding='utf8') as m:m=m.readlines()
if len(m) != 8:
    open(__file__, "w", encoding="utf-8").write("BỐ LÀ ANHNGUYENCODER!")
    raise MemoryError('Anhnguyencoder...')
Anhnguyencoder = vars(globals()['__builtins__'])
"""

loadcode = """
print(' ' * len('Loading...'), end='\\r')
print('Loading...', end='\\r')
"""

builtins = ['__import__', 'print', 'all', 'any', 'ascii', 'bin', 'breakpoint', 'callable', 'chr', 'compile', 'delattr', 'dir', 'divmod', 'eval', 'exec', 'format', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id', 'input', 'isinstance', 'issubclass', 'iter', 'aiter', 'len', 'locals', 'max', 'min', 'next', 'anext', 'oct', 'ord', 'pow', 'print', 'repr', 'round', 'setattr', 'sorted', 'sum', 'vars', 'None', 'Ellipsis', 'NotImplemented', 'False', 'True', 'bool', 'memoryview', 'bytearray', 'bytes', 'classmethod', 'complex', 'dict', 'enumerate', 'filter', 'float', 'frozenset', 'property', 'int', 'list', 'map', 'object', 'range', 'reversed', 'set', 'slice', 'staticmethod', 'str', 'super', 'tuple', 'type', 'zip''open']

class hide(ast.NodeTransformer):

    def visit_Name(self, node):
        if node.id in builtins:
            return ast.Subscript(value=ast.Call(func=ast.Name(id='vars', ctx=ast.Load()), args=[ast.Subscript(value=ast.Call(func=ast.Name(id='globals', ctx=ast.Load()), args=[], keywords=[]), slice=ast.Constant(value='__builtins__'), ctx=ast.Load())], keywords=[]), slice=ast.Constant(value=node.id), ctx=ast.Load())
        return node

def joinstr(f):
    if not isinstance(f, ast.JoinedStr):
        return f
    vl = []
    for i in f.values:
        if isinstance(i, ast.Constant):
            vl.append(i)
        elif isinstance(i, ast.FormattedValue):
            value_expr = i.value
            if i.conversion == 115:
                value_expr = Call(func=Name(id='__meo__', ctx=Load()), args=[value_expr], keywords=[])
            elif i.conversion == 114:
                value_expr = Call(func=Name(id='repr', ctx=Load()), args=[value_expr], keywords=[])
            elif i.conversion == 97:
                value_expr = Call(func=Name(id='ascii', ctx=Load()), args=[value_expr], keywords=[])
            if i.format_spec:
                if isinstance(i.format_spec, ast.JoinedStr):
                    spec_expr = joinstr(i.format_spec)
                elif isinstance(i.format_spec, ast.Constant):
                    spec_expr = i.format_spec
                elif isinstance(i.format_spec, ast.FormattedValue):
                    spec_parts = []
                    spec_value = i.format_spec.value
                    if i.format_spec.conversion == 115:
                        spec_value = Call(func=Name(id='__meo__', ctx=Load()), args=[spec_value], keywords=[])
                    elif i.format_spec.conversion == 114:
                        spec_value = Call(func=Name(id='repr', ctx=Load()), args=[spec_value], keywords=[])
                    elif i.format_spec.conversion == 97:
                        spec_value = Call(func=Name(id='ascii', ctx=Load()), args=[spec_value], keywords=[])
                    spec_expr = spec_value
                else:
                    spec_expr = i.format_spec
                value_expr = Call(func=Name(id='format', ctx=Load()), args=[value_expr, spec_expr], keywords=[])
            elif i.conversion == -1:
                value_expr = Call(func=Name(id='__meo__', ctx=Load()), args=[value_expr], keywords=[])
            vl.append(value_expr)
        elif hasattr(i, 'values') and isinstance(i, ast.JoinedStr):
            vl.append(joinstr(i))
        else:
            vl.append(Call(func=Name(id='__meo__', ctx=Load()), args=[i], keywords=[]))
    if not vl:
        return Constant(value='')
    if len(vl) == 1 and isinstance(vl[0], ast.Constant):
        return vl[0]
    return Call(func=Attribute(value=Constant(value=''), attr='join', ctx=Load()), args=[Tuple(elts=vl, ctx=Load())], keywords=[])

class fstring(ast.NodeTransformer):

    def visit_JoinedStr(self, node):
        node = joinstr(node)
        return node

def _args(name):
    return ast.arguments(posonlyargs=[], args=[ast.arg(arg=name)], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[])

def rb(n=8):
    return ''.join((random.choice(string.ascii_letters) for _ in range(n)))

def obfstr(s):
    OFFSET = random.choice([random.randint(12353, 12355), random.randint(0x1F600, 0x1F64F), random.randint(0x2170, 0x217F)])
    encoded = ''.join((chr((ord(c) ^ 19) + OFFSET) for c in s))
    v = rb()
    fake = ast.Constant('Xin Anh Dung Dec')
    lam = ast.Lambda(args=_args(rb()), body=ast.Call(func=ast.Attribute(value=ast.Call(ast.Name('__meo__', ast.Load()), [], []), attr='join', ctx=ast.Load()), args=[ast.GeneratorExp(elt=ast.Call(ast.Name('chr', ast.Load()), [ast.BinOp(ast.BinOp(ast.Call(ast.Name('ord', ast.Load()), [ast.Name(v, ast.Load())], []), ast.Sub(), ast.Constant(OFFSET)), ast.BitXor(), ast.Constant(19))], []), generators=[ast.comprehension(target=ast.Name(v, ast.Store()), iter=ast.Constant(encoded), ifs=[], is_async=0)])], keywords=[]))
    return ast.Call(lam, [fake], [])

def obfint(i):
    mask = random.randint(1000, 9999)
    scrambled = (i ^ mask) + mask
    fake = ast.Constant('Xin Anh Dung Dec')
    lam = ast.Lambda(args=_args(rb()), body=ast.Call(ast.Name('_minh___', ast.Load()), [ast.BinOp(ast.BinOp(ast.Constant(scrambled), ast.Sub(), ast.Constant(mask)), ast.BitXor(), ast.Constant(mask))], []))
    return ast.Call(lam, [fake], [])

class obfstring(ast.NodeTransformer):

    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value:
            return obfstr(node.value)
        elif isinstance(node.value, int):
            return obfint(node.value)
        return node

nghich = ''.join(random.sample([chr(i) for i in range(0xAC00, 0xD7A4)], 11))
def speed(code):
    code = ast.parse(code) if isinstance(code, str) else code

    class UnicodeObf(ast.NodeTransformer):

        def __init__(self):
            self.injected = False
            self.decoder_name = f'__{nghich}___'

        def obfstringv1(self):
            ord_name = ''.join(map(chr, [111, 114, 100]))
            chr_name = ''.join(map(chr, [99, 104, 114]))
            join_name = ''.join(map(chr, [106, 111, 105, 110]))
            return ast.FunctionDef(name=self.decoder_name, args=ast.arguments(posonlyargs=[], args=[ast.arg(arg='x'), ast.arg(arg='o')], kwonlyargs=[], kw_defaults=[], defaults=[]), body=[ast.Return(value=ast.Call(func=ast.Attribute(value=ast.Constant(''), attr=join_name, ctx=ast.Load()), args=[ast.GeneratorExp(elt=ast.Call(func=ast.Name(id=chr_name, ctx=ast.Load()), args=[ast.BinOp(left=ast.Call(func=ast.Name(id=ord_name, ctx=ast.Load()), args=[ast.Name(id='c', ctx=ast.Load())], keywords=[]), op=ast.Sub(), right=ast.Name(id='o', ctx=ast.Load()))], keywords=[]), generators=[ast.comprehension(target=ast.Name(id='c', ctx=ast.Store()), iter=ast.Name(id='x', ctx=ast.Load()), ifs=[], is_async=0)])], keywords=[]))], decorator_list=[])

        def visit_Module(self, node):
            self.generic_visit(node)
            if not self.injected:
                decoder = self.obfstringv1()
                node.body.insert(0, decoder)
                self.injected = True
            return node

        def visit_Constant(self, node):
            if not isinstance(node.value, str):
                return node
            if not node.value:
                return node
            OFFSET = random.randint(*random.choice([(0x1F600, 0x1F64F), (0x0300, 0x036F), (12353, 12355)]))
            encoded = ''.join(vars(__builtins__)['chr'](vars(__builtins__)['ord'](c) + OFFSET) for c in node.value)
            return ast.Call(func=ast.Name(id=self.decoder_name, ctx=ast.Load()), args=[ast.Constant(encoded), ast.Constant(OFFSET)], keywords=[])
    transformer = UnicodeObf()
    code = transformer.visit(code)
    ast.fix_missing_locations(code)
    return code

def un():
    pool = [chr(i) for i in range(12353, 12355) if chr(i).isidentifier()]
    return random.choice(pool) + ''.join(random.choices(pool, k=8))

def junkcode(code):
    taisao = un()
    minhanh = un()
    djtmemay = un()
    return [ast.Assign(targets=[ast.Name(id=minhanh, ctx=ast.Store())], value=ast.Constant(value=taisao)), ast.Assign(targets=[ast.Name(id=djtmemay, ctx=ast.Store())], value=ast.Constant(value=True)), ast.If(test=ast.BoolOp(op=ast.And(), values=[ast.Compare(left=ast.Name(id=minhanh, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value=taisao)]), ast.Compare(left=ast.Name(id=djtmemay, ctx=ast.Load()), ops=[ast.NotEq()], comparators=[ast.Constant(value=True)])]), body=[ast.Expr(value=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=ast.Constant(value='dit me may')))], orelse=[ast.If(test=ast.BoolOp(op=ast.And(), values=[ast.Compare(left=ast.Name(id=minhanh, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value=taisao)]), ast.Compare(left=ast.Name(id=djtmemay, ctx=ast.Load()), ops=[ast.NotEq()], comparators=[ast.Constant(value=False)])]), body=[ast.Try(body=[ast.Expr(value=ast.Tuple(elts=[ast.BinOp(ast.Constant(1), ast.Div(), ast.Constant(0)), ast.BinOp(ast.Constant(123), ast.Div(), ast.Constant(0)), ast.BinOp(ast.Constant(12312321312), ast.Div(), ast.Constant(0))], ctx=ast.Load()))], handlers=[ast.ExceptHandler(type=None, name=None, body=[code])], orelse=[], finalbody=[])], orelse=[ast.If(test=ast.BoolOp(op=ast.Or(), values=[ast.Compare(left=ast.Name(id=minhanh, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value='gay')]), ast.Compare(left=ast.Name(id=djtmemay, ctx=ast.Load()), ops=[ast.Eq()], comparators=[ast.Constant(value=False)])]), body=[ast.Expr(value=ast.Call(func=ast.Lambda(args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]), body=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[ast.Constant(value='cai lon cha nha may')], keywords=[])), args=[], keywords=[]))], orelse=[ast.While(test=ast.Constant(value=True), body=[ast.Pass()], orelse=[]), ast.Expr(value=ast.Call(func=ast.Name(id='print', ctx=ast.Load()), args=[ast.Constant(value='cai dit thang cha may')], keywords=[]))])])])]

class junk(ast.NodeTransformer):

    def visit_Module(self, node):
        new_body = []
        for stmt in node.body:
            if isinstance(stmt, (ast.FunctionDef, ast.ClassDef)):
                stmt = self.visit(stmt)
            new_body.extend(junkcode(stmt))
        node.body = new_body
        return node

    def visit_FunctionDef(self, node):
        new_body = []
        for stmt in node.body:
            new_body.extend(junkcode(stmt))
        node.body = new_body
        return node

    def visit_ClassDef(self, node):
        new_body = []
        for stmt in node.body:
            new_body.extend(junkcode(stmt))
        node.body = new_body
        return node

def encode(data: bytes):
    out = []
    for b in data:
        out.append(meo[b >> 4])
        out.append(meo[b & 15])
    return ''.join(out)

def gen(s):
    offsets = [random.randint(80,200) for _ in s]
    encoded = [ord(c)+o for c,o in zip(s,offsets)]
    return encoded, offsets

m_vals, m_off = gen("str")
l_vals, l_off = gen("int")

def rb1():
    nums = [random.randint(0xE000, 0xF000) for _ in range(random.randint(3, 6))]
    expr = " + ".join(map(str, nums))
    return f"(lambda: {expr})()"

def rb2():
    return ''.join(random.choices([chr(i) for i in range(44032, 55204) if chr(i).isprintable() and chr(i).isidentifier()], k=10))

#ánh xạ 1
cust = rb1()
tambiet = rb2()
def vip(s, junk=None, max_=2):
    import random
    random.seed()
    if junk is None:
        junk = cust + "!@#6$%.().1.>.ⰲⰲⰲ.?2^#$ⰲⰲⰲ#$56^&*()__AnhNguyenCoder___!@#$%^&ⰲⰲⰲ*@#$ⰲⰲⰲ%()_" + tambiet
    __map__ = {}
    _fmt_ = []
    for i, c in enumerate(s):
        hihi = f"{junk}{i}"
        __map__[hihi] = c
        _fmt_.append(f"%({hihi})s")
        for _ in range(random.randint(1, max_)):
            fake_key = f"{junk}{random.randint(1000,9999)}"
            __map__[fake_key] = junk
    fmt = ''.join(_fmt_)
    return f"('{fmt}' % {__map__})"

def sanh(payload: str):
    return f"""if str(__import__('sys').version[0:4]) != '{str(eval("__import__('sys').version[0:4]"))}':
    print('You need to Install Python {str(eval("__import__('sys').version[0:4]"))}')
    __import__("sys").exit()
__meo__=getattr((lambda:(lambda q:q)(__import__('builtins')))(),''.join((lambda i:chr((i[0]-(i[1]//2))-(i[1]-(i[1]//2))))(p)for p in [(x,y)for x,y in zip({m_vals},{m_off})]))
_minh___=getattr((lambda:(lambda q:q)(__import__('builtins')))(),''.join((lambda i:chr((i[0]-(i[1]//2))-(i[1]-(i[1]//2))))(p)for p in [(x,y)for x,y in zip({l_vals},{l_off})]))
try:__Anhnguyencoder__=lambda __AnhNguyen___:{vip('marshal')};__Anhnguyencoder1__=lambda __AnhNguyen___:{vip('loads')};exec(getattr(__import__(__Anhnguyencoder__('')),__Anhnguyencoder1__(''))(bytes((lambda t,s:[(t.index(s[i])<<4|t.index(s[i+1]))for i in range(0,len(s),2)])({meo!r},"{payload}"))))
except Exception as e:print(e)
except KeyboardInterrupt:pass"""

def main():
    if len(sys.argv) != 2:
        print('Usage: python enc.py <file.py>')
        return
    file = sys.argv[1]
    if not os.path.exists(file):
        print('File not found.')
        return

    with open(file, 'r', encoding='utf-8') as f:
        code = ast.parse(anti+loadcode + f.read())

    print("f_string...")
    tree = fstring().visit(code)
    print("hide builtins")
    tree = hide().visit(tree)
    print("obfstring...")
    code = obfstring().visit(tree)
    tree = speed(code)
    print("Adding Junkcode...")
    code = junk().visit(tree)
    ast.fix_missing_locations(code)

    code = marshal.dumps(compile(ast.unparse(code), 'MiToMa', 'exec'))
    code = encode(code)
    loader = sanh(code)

    out = "obf-" + file

    with open(out, 'w', encoding='utf-8') as f:
        f.write(loader)
    print('Done ->', out)

if __name__ == '__main__':
    main()