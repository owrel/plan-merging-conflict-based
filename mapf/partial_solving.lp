time(1..horizon).

nedge(V,V) :- nvertex(V).
nedge(U,V) :- 
    nvertex(V), 
    nvertex(U), 
    edge(U,V).

at(R,P,0) :- start(R,P).

{ move(R,U,V,T) : nedge(U,V)} 1 :- agent(R), time(T).

at(R,V,T) :- move(R,_,V,T).
          :- move(R,U,_,T), not at(R,U,T-1).

at(R,V,T) :- 
    at(R,V,T-1), 
    not move(R,V,_,T), 
    time(T).

:- {at(R,V,T)}!=1, agent(R), time(T).

:- { at(R,V,T) : agent(R) }  > 1, nvertex(V), time(T).

:- move(_,U,V,T), move(_,V,U,T), U < V.

goal_reached(R) :- at(R,V,horizon), goal(R,V).

#maximize{1,R : goal_reached(R)}.