function [x,y] = fcn(xi,yi,thetai,theta_kb,V_kb,w_kb, P, R, xe)
%#codegen
H=eye(3);
zk = H*[xi;yi;thetai];
Ts = 0.5;

%modelo

F= [Ts*cos(theta_kb)*V_kb 0 0;0 Ts*sin(theta_kb)*V_kb 0;0 0 Ts*w_kb]; %%
%============================

% esto debería ir en un ciclo infinito
% actualización en tiempo (predicción)
xe = F*xe;        % x[n+1|n] 
P = F*P*F';     % P[n+1|n]
% actualización (medidas)
K = P*H'/(H*P*H'); % actualización de ganancia
xe = xe + K*(zk-H*xe);  % x[n|n]
P = (eye(3)-K*H)*P;  % P[n|n]



ye=H*xe; %salida estimada

x=ye(1);
y=ye(2);
%theta=ye(3);
%errcov = H*P*H'; % actualización error covarianza

  