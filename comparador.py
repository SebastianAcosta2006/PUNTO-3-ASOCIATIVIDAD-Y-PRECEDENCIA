import re

class Lexer:
    def __init__(self, text):
        self.tokens = re.findall(r'\d+\.?\d*|[+\-*/^()]', text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        tok = self.tokens[self.pos]; self.pos += 1; return tok

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def eval(self):
        if self.left is None and self.right is None:
            return float(self.value)
        l, r = self.left.eval(), self.right.eval()
        ops = {'+': l+r, '-': l-r, '*': l*r, '/': l/r, '^': l**r}
        return ops[self.value]

    def to_str(self):
        if self.left is None and self.right is None:
            return str(int(float(self.value)))
        l = self.left.to_str()
        r = self.right.to_str()
        return f"({l}{self.value}{r})"

def print_tree(node, prefix="", is_left=True):
    if node is not None:
        connector = "├── " if is_left else "└── "
        print(prefix + connector + str(node.value))
        if node.left or node.right:
            ext = "│   " if is_left else "    "
            if node.left:  print_tree(node.left,  prefix + ext, True)
            if node.right: print_tree(node.right, prefix + ext, False)

# ─────────────────────────────────────────────────────────────
# GRAMÁTICA 1: Asoc. IZQUIERDA, Precedencia ESTÁNDAR (^>*/> +-)
# ─────────────────────────────────────────────────────────────
class ParserG1:
    def __init__(self, lexer): self.l = lexer
    def parse(self): return self.expr()
    def expr(self):
        n = self.term()
        while self.l.peek() in ('+', '-'):
            op = self.l.consume(); n = Node(op, n, self.term())
        return n
    def term(self):
        n = self.expo()
        while self.l.peek() in ('*', '/'):
            op = self.l.consume(); n = Node(op, n, self.expo())
        return n
    def expo(self):
        n = self.base()
        while self.l.peek() == '^':
            op = self.l.consume(); n = Node(op, n, self.base())
        return n
    def base(self):
        if self.l.peek() == '(':
            self.l.consume(); n = self.expr(); self.l.consume(); return n
        return Node(self.l.consume())

# ─────────────────────────────────────────────────────────────
# GRAMÁTICA 2: Asoc. DERECHA, Precedencia ESTÁNDAR (^>*/> +-)
# ─────────────────────────────────────────────────────────────
class ParserG2:
    def __init__(self, lexer): self.l = lexer
    def parse(self): return self.expr()
    def expr(self):
        n = self.term()
        if self.l.peek() in ('+', '-'):
            op = self.l.consume(); n = Node(op, n, self.expr())
        return n
    def term(self):
        n = self.expo()
        if self.l.peek() in ('*', '/'):
            op = self.l.consume(); n = Node(op, n, self.term())
        return n
    def expo(self):
        n = self.base()
        if self.l.peek() == '^':
            op = self.l.consume(); n = Node(op, n, self.expo())
        return n
    def base(self):
        if self.l.peek() == '(':
            self.l.consume(); n = self.expr(); self.l.consume(); return n
        return Node(self.l.consume())

# ─────────────────────────────────────────────────────────────
# GRAMÁTICA 3: Asoc. IZQUIERDA, Precedencia INVERSA (+->*/>^)
# ─────────────────────────────────────────────────────────────
class ParserG3:
    def __init__(self, lexer): self.l = lexer
    def parse(self): return self.expr()
    def expr(self):          # ^ tiene MENOR precedencia
        n = self.term()
        while self.l.peek() == '^':
            op = self.l.consume(); n = Node(op, n, self.term())
        return n
    def term(self):          # */ precedencia media
        n = self.suma()
        while self.l.peek() in ('*', '/'):
            op = self.l.consume(); n = Node(op, n, self.suma())
        return n
    def suma(self):          # +- MAYOR precedencia
        n = self.base()
        while self.l.peek() in ('+', '-'):
            op = self.l.consume(); n = Node(op, n, self.base())
        return n
    def base(self):
        if self.l.peek() == '(':
            self.l.consume(); n = self.expr(); self.l.consume(); return n
        return Node(self.l.consume())

# ─────────────────────────────────────────────────────────────
# GRAMÁTICA 4: Asoc. DERECHA, Precedencia INVERSA (+->*/>^)
# ─────────────────────────────────────────────────────────────
class ParserG4:
    def __init__(self, lexer): self.l = lexer
    def parse(self): return self.expr()
    def expr(self):          # ^ tiene MENOR precedencia, asoc. DERECHA
        n = self.term()
        if self.l.peek() == '^':
            op = self.l.consume(); n = Node(op, n, self.expr())
        return n
    def term(self):          # */ precedencia media, asoc. DERECHA
        n = self.suma()
        if self.l.peek() in ('*', '/'):
            op = self.l.consume(); n = Node(op, n, self.term())
        return n
    def suma(self):          # +- MAYOR precedencia, asoc. DERECHA
        n = self.base()
        if self.l.peek() in ('+', '-'):
            op = self.l.consume(); n = Node(op, n, self.suma())
        return n
    def base(self):
        if self.l.peek() == '(':
            self.l.consume(); n = self.expr(); self.l.consume(); return n
        return Node(self.l.consume())

# ─────────────────────────────────────────────────────────────
# EJECUCIÓN Y COMPARACIÓN
# ─────────────────────────────────────────────────────────────

grammars = [
    ("G1", "Asoc. IZQUIERDA + Prec. ESTÁNDAR  (^>*/> +-)", ParserG1),
    ("G2", "Asoc. DERECHA  + Prec. ESTÁNDAR  (^>*/> +-)", ParserG2),
    ("G3", "Asoc. IZQUIERDA + Prec. INVERSA  (+->*/>^)", ParserG3),
    ("G4", "Asoc. DERECHA  + Prec. INVERSA  (+->*/>^)", ParserG4),
]

cadenas = [
    "2 + 3 * 4 - 5 / 1 ^ 2",
    "2 ^ 3 ^ 2",
]

for cadena in cadenas:
    print("\n" + "═" * 70)
    print(f"  CADENA DE PRUEBA: {cadena}")
    print("═" * 70)

    for gid, gdesc, GParser in grammars:
        print(f"\n--- {gid}: {gdesc} ---")
        lexer = Lexer(cadena)
        parser = GParser(lexer)
        arbol = parser.parse()
        agrupacion = arbol.to_str()
        resultado = arbol.eval()
        print(f"  Agrupación implícita : {agrupacion}")
        print(f"  Árbol:")
        print_tree(arbol, "    ", False)
        print(f"  Resultado numérico   : {resultado}")

# ─────────────────────────────────────────────────────────────
# TABLA RESUMEN
# ─────────────────────────────────────────────────────────────
print("\n" + "═" * 70)
print("TABLA RESUMEN COMPARATIVA")
print("═" * 70)
header = f"{'Gramática':<8} {'Asociatividad':<14} {'Precedencia':<12} {'Cadena 1':>12} {'Cadena 2':>10}"
print(header)
print("-" * 70)

for gid, gdesc, GParser in grammars:
    asoc = "Izquierda" if "IZQUIERDA" in gdesc else "Derecha"
    prec = "Estándar" if "ESTÁNDAR" in gdesc else "Inversa"
    resultados = []
    for cadena in cadenas:
        lexer = Lexer(cadena)
        parser = GParser(lexer)
        arbol = parser.parse()
        resultados.append(arbol.eval())
    print(f"{gid:<8} {asoc:<14} {prec:<12} {resultados[0]:>12.1f} {resultados[1]:>10.1f}")

print("-" * 70)
print("\nNota: Los valores DISTINTOS entre gramáticas con la misma cadena")
print("demuestran el impacto de la asociatividad y la precedencia en el")
print("análisis sintáctico.")
