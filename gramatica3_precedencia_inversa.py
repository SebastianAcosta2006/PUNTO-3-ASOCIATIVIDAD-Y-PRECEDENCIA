"""
GRAMÁTICA 3: Asociatividad IZQUIERDA con precedencia INVERSA (no estándar)
Precedencia inversa (mayor a menor): + - > * / > ^
Asociatividad: IZQUIERDA
Cadena de prueba: 2 + 3 * 4 - 5 / 1 ^ 2
"""

# ============================================================
# ANALIZADOR DESCENDENTE RECURSIVO
# En gramáticas LL, mayor precedencia = producción más profunda
# Precedencia INVERSA: +- tienen mayor precedencia, ^ la menor
#
# Gramática BNF con precedencia invertida:
#   expr   -> term  ['^' term]*          <-- ^ tiene MENOR precedencia
#   term   -> suma  [('*' | '/') suma]*  <-- */ tiene precedencia media
#   suma   -> base  [('+' | '-') base]*  <-- +- tienen MAYOR precedencia
#   base   -> NUMBER | '(' expr ')'
# ============================================================

import re

class Lexer:
    def __init__(self, text):
        self.tokens = re.findall(r'\d+\.?\d*|[+\-*/^()]', text)
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def eval(self):
        if self.left is None and self.right is None:
            return float(self.value)
        l = self.left.eval()
        r = self.right.eval()
        if self.value == '+': return l + r
        if self.value == '-': return l - r
        if self.value == '*': return l * r
        if self.value == '/': return l / r
        if self.value == '^': return l ** r


class Parser:
    """
    Gramática con asociatividad IZQUIERDA y precedencia INVERSA:
      +- > */ > ^
    Mayor precedencia = producción MÁS PROFUNDA en el árbol.
    
    expr   -> term ('^' term)*           <-- ^ queda en la raíz
    term   -> suma (('*' | '/') suma)*   <-- */ queda en nivel medio
    suma   -> base (('+' | '-') base)*   <-- +- queda más profundo
    base   -> NUMBER | '(' expr ')'
    """
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        return self.expr()

    def expr(self):
        # MENOR precedencia: ^
        node = self.term()
        while self.lexer.peek() == '^':
            op = self.lexer.consume()
            right = self.term()
            node = Node(op, node, right)
        return node

    def term(self):
        # PRECEDENCIA MEDIA: * /
        node = self.suma()
        while self.lexer.peek() in ('*', '/'):
            op = self.lexer.consume()
            right = self.suma()
            node = Node(op, node, right)
        return node

    def suma(self):
        # MAYOR precedencia: + -
        node = self.base()
        while self.lexer.peek() in ('+', '-'):
            op = self.lexer.consume()
            right = self.base()
            node = Node(op, node, right)
        return node

    def base(self):
        tok = self.lexer.peek()
        if tok == '(':
            self.lexer.consume()
            node = self.expr()
            self.lexer.consume()  # ')'
            return node
        else:
            return Node(self.lexer.consume())


def print_tree(node, prefix="", is_left=True):
    if node is not None:
        print(prefix + ("├── " if is_left else "└── ") + str(node.value))
        if node.left or node.right:
            if node.left:
                print_tree(node.left, prefix + ("│   " if is_left else "    "), True)
            if node.right:
                print_tree(node.right, prefix + ("│   " if is_left else "    "), False)


if __name__ == "__main__":
    cadena = "2 + 3 * 4 - 5 / 1 ^ 2"
    print("=" * 60)
    print("GRAMÁTICA 3: Asociatividad IZQUIERDA, precedencia INVERSA")
    print("Precedencia invertida: +- > */ > ^")
    print(f"Cadena de prueba: {cadena}")
    print("=" * 60)

    lexer = Lexer(cadena)
    parser = Parser(lexer)
    arbol = parser.parse()

    print("\nÁrbol de análisis sintáctico:")
    print_tree(arbol, "", False)

    resultado = arbol.eval()
    print(f"\nResultado evaluado: {resultado}")
    print("\nNota: Con precedencia invertida, + y - se evalúan PRIMERO,")
    print("luego * y /, y finalmente ^.")
    print("La expresión se interpreta como: ((2+3) * (4-5)) / (1^2)")
    print("= (5 * -1) / 1 = -5.0")

    # Segunda prueba
    cadena2 = "2 ^ 3 ^ 2"
    print("\n" + "=" * 60)
    print(f"Prueba de asociatividad pura: {cadena2}")
    print("=" * 60)
    lexer2 = Lexer(cadena2)
    parser2 = Parser(lexer2)
    arbol2 = parser2.parse()
    print("\nÁrbol de análisis sintáctico:")
    print_tree(arbol2, "", False)
    print(f"\nResultado: {arbol2.eval()}")
    print("Con precedencia inversa y asoc. izquierda: (2^3)^2 = 64")
