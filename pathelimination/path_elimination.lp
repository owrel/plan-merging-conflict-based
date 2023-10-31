to_kill(R,I) :- 
    critical_vertex(V,T), 
    critical_agent(R,V,T), 
    at(R,I,V,T).