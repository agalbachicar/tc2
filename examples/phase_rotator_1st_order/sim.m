% Limpiamos el entorno de trabajo
close all
clear all
clc % En Matlab puede ser cls

% Loads the control packag, note that this is not necessary in Matlab
pkg load control

% Definimos los valores de los componentes
R1 = 1e3;
R2 = 1e3;
R3 = 1e3;
C4 = 1e-6;

disp('Constante de ganancia del inversor');
K_inv = R2 / R1

% Cargamos la funcion transferencia
s = tf('s');

disp('Funcion transferencia');
H = - (K_inv / (R3 * C4) - s) / (1. / (R3 * C4) + s)

% Graficamos el diagrama de polos y ceros
figure;
pzmap(H);

% Graficamos la respuesta en frecuencia para el modulo y la fase.
figure;
bode(H);

% Pregunta: ¿que valores deberia tener R3 y C4 para tener una rotacion de fase
% de 120° a 1000Hz la salida respecto a la entrada?

