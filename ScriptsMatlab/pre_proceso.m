function [theta,V,w] = pre_proceso(wd,wi)
r=0.625;
b=19.5;
vi= r*wi;
vd= r*wd;
V = (vd+vi)/2;
w = (wi-wd)/b;
theta = w*r;