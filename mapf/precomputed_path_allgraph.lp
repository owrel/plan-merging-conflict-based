at(R,V,T) :-
    selected_path(R,I),
    at(R,I,V,T).

nvertex(V) :- vertex(V).
nedge(U,V) :- edge(U,V).