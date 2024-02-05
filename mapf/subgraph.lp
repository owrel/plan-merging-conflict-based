#defined path_with_lowest_summed_heatmap/2.

nvertex(V) :- 
    at(R,I,V,_),
    path_with_lowest_summed_heatmap(R,I), 
    not selected_agent(R).

nvertex(V) :- selected_path(R,I), at(R,I,V,_).
nedge(U,V) :-
    edge(U,V),
    nvertex(U),
    nvertex(V).


