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

selected_vertex_for_diamond(V) :- collision((R1,P1),_,T), at(R1,P1,V,T).
selected_path_for_corridor(R,I) :- collision((R,I),_,T).