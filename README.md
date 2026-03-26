# PUNTO-3-ASOCIATIVIDAD-Y-PRECEDENCIA

Análisis de Asociatividad y Precedencia en Gramáticas Aritméticas

Descripción

Este proyecto implementa y compara **cuatro versiones de una gramática aritmética** que demuestran cómo la asociatividad (izquierda/derecha) y la precedencia de operadores (estándar/inversa) afectan el análisis sintáctico y los resultados de evaluación de expresiones aritméticas.

Estructura del Proyecto

asociatividad_precedencia/
│
├── gramatica1_izquierda.py          # G1: Asoc. Izquierda + Prec. Estándar
├── gramatica2_derecha.py            # G2: Asoc. Derecha   + Prec. Estándar
├── gramatica3_precedencia_inversa.py # G3: Asoc. Izquierda + Prec. Inversa
├── gramatica4_derecha_inversa.py    # G4: Asoc. Derecha   + Prec. Inversa
├── comparador.py                    # Ejecuta y compara las 4 gramáticas
└── README.md                        # Este archivo


Gramáticas Implementadas

G1 – Asociatividad Izquierda, Precedencia Estándar
Precedencia: `^` > `*/` > `+-`
Asociatividad: izquierda (bucle iterativo)
  `2 ^ 3 ^ 2` → `(2^3)^2 = 64`

G2 – Asociatividad Derecha, Precedencia Estándar
Precedencia: `^` > `*/` > `+-`
  Asociatividad: derecha (recursión directa)
  2 ^ 3 ^ 2` → `2^(3^2) = 512` ← comportamiento matemático real

G3 – Asociatividad Izquierda, Precedencia Inversa
Precedencia: `+-` > `*/` > `^`
  Asociatividad: izquierda (bucle iterativo)
  2 + 3 * 4 - 5 / 1 ^ 2` → `((2+3)*(4-5)/1)^2 = 25`

G4 – Asociatividad Derecha, Precedencia Inversa
Precedencia: `+-` > `*/` > `^`
  Asociatividad: derecha (recursión directa)
  2 + 3 * 4 - 5 / 1 ^ 2` → `((2+3)*((4-5)/1))^2 = 25`

Cómo Ejecutar

Requisitos
Python 3

Ejecutar una gramática individual

ash
python3 gramatica1_izquierda.py
python3 gramatica2_derecha.py
python3 gramatica3_precedencia_inversa.py
python3 gramatica4_derecha_inversa.py


Ejecutar la comparación completa

bash
python3 comparador.py
Cadenas de Prueba

| Cadena                  | Propósito                                |
|-------------------------|------------------------------------------|
| `2 + 3 * 4 - 5 / 1 ^ 2`| Verifica diferencias de precedencia      |
| `2 ^ 3 ^ 2`             | Verifica diferencias de asociatividad pura|

## Tabla de Resultados

| Gramática | Asociatividad | Precedencia | `2+3*4-5/1^2` | `2^3^2` |
|-----------|---------------|-------------|---------------|---------|
| G1        | Izquierda     | Estándar    | **9.0**       | **64**  |
| G2        | Derecha       | Estándar    | **9.0**       | **512** |
| G3        | Izquierda     | Inversa     | **25.0**      | **64**  |
| G4        | Derecha       | Inversa     | **25.0**      | **512** |

Observaciones Clave

1. La precedencia determina el resultado de la cadena mixta**: G1/G2 producen 9.0 (correcta matemáticamente), mientras G3/G4 producen 25.0 porque +- tienen mayor precedencia.

2. La asociatividad determina el resultado de 2^3^2: Las gramáticas con asociatividad izquierda producen 64 (incorrecto matemáticamente), mientras las de derecha producen 512 (correcto matemáticamente).

3. Implementación técnica:
   Asociatividad izquierda bucle while en el parser
     Asociatividad derecha recursión directa (llamada a sí misma) en el parser
     Mayor precedencia producción más profunda** en la gramática

Principio Fundamental de las Gramáticas LL

En un analizador descendente recursivo (LL):

Los operadores con **mayor precedencia** deben estar en las producciones **más profundas** (más cercanas a los terminales).
Los operadores con **menor precedencia** deben estar en las producciones **más altas** (más cercanas al símbolo inicial).
La asociatividad izquierda se implementa con while (iteración).
La asociatividad derecha se implementa con recursión a la derecha.

