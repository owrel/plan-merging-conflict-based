path_killed(R,I) :- to_kill(R,I).

agent_killed(R) :- P=PK,
    P = #count{1,I : at(R,I,_,_)}, 
    PK = #count{1,I : path_killed(R,I)}, 
    agent(R).