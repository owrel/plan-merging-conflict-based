time(1..horizon).

{at(V,0) : vertex(V)} = 1.

{ move(U,V,T) : edge(U,V)} 1 :- time(T).

at(V,T) :- move(_,V,T).
        :- move(U,_,T), not at(U,T-1).

:- { at(V,T) } != 1, time(T).

at(V,T) :-
    at(V,T-1),
    not move(V,_,T),
    time(T).


current_agent(R) :- at(V,0), start(R,V).
at(GV,T+1) :- at(GV,T), time(T+1), goal(R,GV), current_agent(R).


#show at/2.
