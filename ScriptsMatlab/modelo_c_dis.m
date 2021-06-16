function [x,y,theta] = modelo_dis(xk,yk,thetak,V_k,w_k,theta_k)
Ts=0.5;
F=eye(3); %%matriz identidad
Fk= [xk;yk;thetak]; %% Las inicializamos en 0 ya que partimos desde el origen
B= [Ts*cos(theta_k) 0; Ts*sin(theta_k) 0; 0 Ts]; %%
u= [ V_k; w_k];

out = (Fk)+(B*u);
x=out(1);
y=out(2);
theta=out(3);