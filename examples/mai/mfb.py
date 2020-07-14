from sympy import *
from sympy.plotting import plot
from sympy.codegen.cfunctions import log10
import matplotlib.pyplot as plt
import numpy as np
# https://docs.sympy.org/latest/install.html
# conda install sympy
# conda install mpmath

# Sobre matrices: https://docs.sympy.org/latest/tutorial/matrices.html

def get_passive_mai(Y_a, Y_b, Y_c, Y_d, Y_e):
  return Matrix([[Y_a, -Y_a, 0, 0, 0],\
                 [-Y_a, Y_a + Y_b + Y_c + Y_d, -Y_c, -Y_d, -Y_b],\
                 [0, -Y_c, Y_c+Y_e, Y_e, 0],\
                 [0, -Y_d, -Y_e, Y_d+Y_e, 0],\
                 [0, -Y_b, 0, 0, Y_b]])

def get_active_mai(A0, Y_i, Y_o):
  return Matrix([[0, 0, 0, 0, 0],\
                 [0, 0, 0, 0, 0],\
                 [0, 0, Y_i, 0, -Y_i],\
                 [0, 0, A0 * Y_o, Y_o, -A0 * Y_o - Y_o],\
                 [0, 0, -Y_i - A0 * Y_o, -Y_o, Y_i + Y_o + A0 * Y_o]])

def get_mfb_mai(Y_a, Y_b, Y_c, Y_d, Y_e, A0, Y_i, Y_o):
  return get_passive_mai(Y_a, Y_b, Y_c, Y_d, Y_e) + get_active_mai(A0, Y_i, Y_o)

# Para mejorar la impresion
init_printing()

# Defino simbolos
Ga = Symbol('Ga')
Cb = Symbol('Cb')
Gc = Symbol('Gc')
Gd = Symbol('Gd')
Ce = Symbol('Ce')
s = Symbol('s')

A0 = Symbol('A0')
Y_i = Symbol('Y_i')
Y_o = Symbol('Y_o')

Y_45_15 = get_mfb_mai(Ga, s*Cb, Gc, Gd, s*Ce, A0, Y_i, Y_o)
Y_45_15.row_del(4)
Y_45_15.row_del(0)
Y_45_15.col_del(4)
Y_45_15.col_del(3)
print('Y_45_15')
print(Y_45_15)

Y_15_15 = get_mfb_mai(Ga, s*Cb, Gc, Gd, s*Ce, A0, Y_i, Y_o)
Y_15_15.row_del(4)
Y_15_15.row_del(0)
Y_15_15.col_del(4)
Y_15_15.col_del(0)
print('Y_15_15')
print(Y_15_15)

V_15_45 = (-1.0)**(-1.0-5.0-4.0-5.0) * Y_45_15.det() / Y_15_15.det()
V_15_45 = cancel(V_15_45)
print('La transferencia de tension es:')
print(V_15_45)