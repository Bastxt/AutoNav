%%Modelo discretizado en representaicon de estados 
%% El modelo continuo que teniamos 
%%   x= V*cos(theta)
%%   y= V*sen(theta)
%%   Theta = W
%% Para la representacion de variables de estado tenemos la sieguiente ecuacion
%% x'(t) = Ax + Bu 
%% y (t) = Cx + Du
%% x= Vector de estado seran las vairables que deseamos hallar o resultantes
%% A = Matriz de estado Nosotros las vamos a suponer como una matriz identidad
%% B = Matriz de entrada
%% u = Variables de entrada
%% y = Vector de salida
%% C = Matriz de salida (relacion entre la salidas)
%% D = Matriz de transferencia

A=eye(3);
F=[Ts 0;ts 0;0 ts]
x= [0; 0; 0;]; %% Las inicializamos en 0 ya que partimos desde el origen
B= [Ts*cos(theta_k) 0; Ts*sin(theta_k) 0; 0 Ts]; %%
u= [ V_k; w_k;];

open('Modelo_Dicreto_SS');
sim('Modelo_Dicreto_SS');


