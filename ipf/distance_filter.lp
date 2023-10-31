#const npath = 5.
{dpath(R,I): at(R,I,_,_)} npath :- agent(R).
#maximize {1@1,R,I : dpath(R,I)}.


dpath(R,I,V,T) :- dpath(R,I), at(R,I,V,T).
dist(R,I1,I2,T, (X1-X2)*(X1-X2) + (Y1-Y2)*(Y1-Y2)) :-
dpath(R,I1,(X1,Y1),T),
dpath(R,I2,(X2,Y2),T), I1!=I2.
dsum(R,DS) :-
    DS=#sum{D:dist(R,I1,I2,_,D), dpath(R,I1), dpath(R,I2)},
    agent(R).

#maximize {1@2,D : dsum(R,D)}.