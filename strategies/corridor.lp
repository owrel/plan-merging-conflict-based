#const corridor_level = 2.

corridor(V,0) :- selected_path_for_corridor(R,I), at(R,I,V,_).
corridor(V,K+1) :-
    K < corridor_level,
    corridor(U,K),
    edge(U,V).
nvertex(V) :- corridor(V,_).