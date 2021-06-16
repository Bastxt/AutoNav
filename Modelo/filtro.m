function [x,y,theta] = filtro(y)
%FILTRO Summary of this function goes here
%   Detailed explanation goes here

Ts=0.5;

B= [Ts*cos(theta_k) 0; Ts*sin(theta_k) 0; 0 Ts]; %%
u= [ V_k; w_k;];

F=B*u; 
H=eye(3);

persistent xe;
persistent P;
persistent K;
persistent R;

if isempty(xe)
        % R=diag(rand(3,1)); %aleatorio
        R=diag([225 16 0.04]); %del ejemplo
        xe = zeros(3,1);
end

if isempty(P)
        P=rand(3);
end

xe = F*xe;        % x[n+1|n]
P = F*P*F';     % P[n+1|n]

% actualización (medidas)
K = P*H'/(H*P*H'+R); % actualización de ganancia
xe = xe + K*(y-H*xe);  % x[n|n]
P = (eye(3)-K*H)*P;  % P[n|n]

ye=H*xe; %salida estimada
x=ye(1);
y=ye(2);
theta=ye(3);
errcov = H*P*H'; % actualización error covarianza

end

