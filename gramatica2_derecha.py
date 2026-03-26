"""
GRAMÁTICA 2: Asociatividad por DERECHA con precedencia matemática estándar
Precedencia (mayor a menor): ^ > * / > + -
Asociatividad: DERECHA para todos los operadores
Cadena de prueba: 2 + 3 * 4 - 5 / 1 ^ 2
"""

# ============================================================
# ANALIZADOR DESCENDENTE RECURSIVO - ASOCIATIVIDAD DERECHA
# Gramática BNF:
#   expr   -> term   ('+' | '-') expr  | term
#   term   -> expo   ('*' | '/') term  | expo
#   expo   -> base   '^' expo          | base   <-- recursión derecha
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
    Gramática con asociatividad DERECHA y precedencia estándar:
      expr   -> term ('+' | '-') expr   | term
      term   -> expo ('*' | '/') term   | expo
      expo   -> base '^' expo           | base   <-- recursión DERECHA
      base   -> NUMBER | '(' expr ')'

    La recursión a la derecha en la misma regla produce
    árboles que se agrupan por la derecha:
      a + b + c  =>  a + (b + c)
      a ^ b ^ c  =>  a ^ (b ^ c)
    """
    def __init__(self, lexer):
        self.lexer = lexer

    def parse(self):
        return self.expr()

    def expr(self):
        # expr -> term (('+' | '-') expr)?
        node = self.term()
        if self.lexer.peek() in ('+', '-'):
            op = self.lexer.consume()
            right = self.expr()          # recursión DERECHA
            node = Node(op, node, right)
        return node

    def term(self):
        # term -> expo (('*' | '/') term)?
        node = self.expo()
        if self.lexer.peek() in ('*', '/'):
            op = self.lexer.consume()
            right = self.term()          # recursión DERECHA
            node = Node(op, node, right)
        return node

    def expo(self):
        # expo -> base ('^' expo)?       [ASOCIATIVIDAD DERECHA]
        node = self.base()
        if self.lexer.peek() == '^':
            op = self.lexer.consume()
            right = self.expo()          # recursión DERECHA
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
    print("GRAMÁTICA 2: Asociatividad DERECHA")
    print("Precedencia estándar: ^ > */ > +-")
    print(f"Cadena de prueba: {cadena}")
    print("=" * 60)

    lexer = Lexer(cadena)
    parser = Parser(lexer)
    arbol = parser.parse()

    print("\nÁrbol de análisis sintáctico:")
    print_tree(arbol, "", False)

    resultado = arbol.eval()
    print(f"\nResultado evaluado: {resultado}")

    # Segunda prueba
    cadena2 = "2 ^ 3 ^ 2"
    print("\n" + "=" * 60)
    print(f"Prueba de asociatividad pura: {cadena2}")
    print("Con asociatividad DERECHA: 2^(3^2) = 2^9 = 512")
    print("=" * 60)
    lexer2 = Lexer(cadena2)
    parser2 = Parser(lexer2)
    arbol2 = parser2.parse()
    print("\nÁrbol de análisis sintáctico:")
    print_tree(arbol2, "", False)
    print(f"\nResultado: {arbol2.eval()}")
    print("Interpretación: (2^(3^2)) = 2^9 = 512  ✓ Asociatividad DERECHA")
