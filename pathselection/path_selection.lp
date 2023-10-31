% Defining collision & possible_path
possible_path(R,I):- at(R,I,_,_), not path_killed(R,I).
% Constructing a (partial) plan
{selected_path(R,I) : possible_path(R,I) }1 :- agent(R).

collision((R1,P1),(R2,P2),T) :-
    R1 != R2,
    at(R1,P1,V,T),
    at(R2,P2,V,T),
    selected_path(R1,P1),
    selected_path(R2,P2).

collision((R1,P1),(R2,P2),T) :-
    R1 != R2,
    at(R1,P1,V1,T),
    at(R1,P1,V2,T+1),
    at(R2,P2,V2,T),
    at(R2,P2,V1,T+1),
    selected_path(R1,P1),
    selected_path(R2,P2).

:- collision((R1,P1),(R2,P2),_),
    selected_path(R1,P1),
    selected_path(R2,P2).



selected_agent(R) :- selected_path(R,_).
#maximize {1@1,R : selected_path(R,_)}.