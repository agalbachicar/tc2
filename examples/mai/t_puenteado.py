from sympy import *

# https://docs.sympy.org/latest/install.html
# conda install sympy
# conda install mpmath

# Sobre matrices: https://docs.sympy.org/latest/tutorial/matrices.html

def eval_mai(G1, G2, C1, C2):
  return Matrix([[s*C1+G1, -G1,        -s*C1,    0   ], \
                 [-G1,     G1+G2+s*C2, -G2,  -   s*C2], \
                 [-s*C1,   -G2,         s*C1+G2, 0   ], \
                 [0,       -s*C2,       0,       s*C2]])


def eval_f_in_s(f, attributes, ww):
  f_eval = []
  for w in ww:
    attributes['s'] = w*I
    f_eval.append(f.evalf(subs=attributes))
  return f_eval


# Para mejorar la impresion
init_printing()

# Defino simbolos
G1 = Symbol('G1')
G2 = Symbol('G2')
C1 = Symbol('C1')
C2 = Symbol('C2')
s = Symbol('s')

# Cargo la MAI
print('Matriz admitancia indefinida para el T puenteado.')
print(eval_mai(G1, G2, C1, C2))

# Computamos la transferencia de tension.
# Recordamos la expresion:
# $ V_{14}^{34} = (-1)^{-1-4-3-4} \frac{Y_{14}^{34}}{Y_{14}^{14}} $

# Cargo la matriz definida del numerador.
Y_14_34 = eval_mai(G1, G2, C1, C2)
Y_14_34.row_del(3)
Y_14_34.row_del(2)
Y_14_34.col_del(3)
Y_14_34.col_del(0)

# Cargo la matriz definida del denominador.
Y_14_14 = eval_mai(G1, G2, C1, C2)
Y_14_14.row_del(3)
Y_14_14.row_del(0)
Y_14_14.col_del(3)
Y_14_14.col_del(0)

# Computo la transferencia
V_14_34 = (-1.0)**(-1.0-4.0-3.0-4.0) * Y_14_34.det() / Y_14_14.det()
V_14_34 = cancel(V_14_34)
print('La transferencia de tension es:')
print(V_14_34)
