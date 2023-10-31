#const diamond_level = 2.

diamond(V,0) :- selected_vertex_for_diamond(V).

diamond(V,S+1) :- 
    diamond(U,S), 
    S<diamond_level, 
    edge(U,V).

nvertex(V) :- diamond(V,_).