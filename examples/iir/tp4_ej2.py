import cmath
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

# Datos del a)
fc = 1e3                      ; print('fc: {}'.format(fc))
w0 = 2. * np.pi * fc          ; print('w0: {}'.format(w0))
Q = 1. / np.sqrt(2.)          ; print('Q:  {}'.format(Q))
fs = 100e3                    ; print('fs: {}'.format(fs))

# Constantes utiles 
alpha = w0 ** 2.              ; print('alpha: {}'.format(alpha))
beta = w0 * 2. * fs / Q       ; print('beta: {}'.format(beta))
gamma = 4. * (fs ** 2.)       ; print('gamma: {}'.format(gamma))

# Coeficientes del filtro
k = alpha / (alpha + beta + gamma) ; print('k: {}'.format(k))
num = k * np.array([1., 2., 1.]) ; print('Num: {}'.format(num))
den = np.array([1., 2*(alpha - gamma)/(alpha + beta + gamma), (alpha - beta + gamma)/(alpha + beta + gamma)]) ; print('Den: {}'.format(den))

# Respuesta del filtro
w, h = signal.freqz(num, den, worN = 512, whole = False)

# Respuesta en frecuencia del filtro
fig, axs = plt.subplots(2)
fig.suptitle('Respuesta de un Butterworth de 2do orden fc={}KHz y fs={}KHz'.format(fc, fs))
axs[0].set_title('Respuesta de modulo')
axs[0].semilogx(w, 20 * np.log10(abs(h)), 'b')
axs[0].set_ylabel('|H| [dB]', color='b')
axs[0].set_xlabel('Ω [rad/sample]')
axs[0].grid()

axs[1].set_title('Respuesta de fase')
axs[1].semilogx(w, [cmath.phase(hh) for hh in h], 'b')
axs[1].set_ylabel('arg(H) [rad]', color='b')
axs[1].set_xlabel('Ω [rad/sample]')
axs[1].grid()
plt.show()

# Polos y ceros del filtro
zeros = np.roots(num)
poles = np.roots(den)
print('Ceros: {}'.format(zeros))
print('Polos: {}'.format(poles))

fig, ax = plt.subplots()
fig.suptitle('Polos y ceros')
unit_circle = plt.Circle((0.,0.), 1., fill=False, color='black')
ax.add_patch(unit_circle)
ax.scatter([hh.real for hh in zeros], [hh.imag for hh in zeros], marker='o', color='b')
ax.scatter([hh.real for hh in poles], [hh.imag for hh in poles], marker='x', color='b')
ax.set_xlabel('x')
ax.set_ylabel('jy')
ax.grid()
plt.show()

# Ufff, cuantas lineas de codigo. Siempre es a mano???
num_s = [w0**2.]
den_s = [1., w0/Q, w0**2]

num_z, den_z = signal.bilinear(num_s, den_s, fs)
print('Num: {}'.format(num_z))
print('Den: {}'.format(den_z))


