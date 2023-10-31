#const npaths=5.
#const horizon=15.

agent(R,1..npaths) :- agent(R).
time(1..horizon).

at(R,I,P,0) :- start(R,P), agent(R,I).

{move(R,I,U,V,T) : edge(U,V)} 1 :- agent(R,I), time(T).

at(R,I,V,T) :- move(R,I,_,V,T).
            :- move(R,I,U,_,T), not at(R,I,U,T-1).

at(R,I,V,T) :- at(R,I,V,T-1),
    not move(R,I,V,_,T),
    time(T).

:- { at(R,I,V,T) }!=1, agent(R,I), time(T).

:- goal(R,V), not at(R,_,V,horizon).

#show at/4.