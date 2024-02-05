#const n_paths_per_agent = 1.

{s_paths(R,I):at(R,I,_,_)} n_paths_per_agent :- agent(R).


path_killed(R,I) :- at(R,I,_,_), not s_paths(R,I).
selected_path(R,I) :- at(R,I,_,_), s_paths(R,I).
selected_agent(R) : selected_path(R,_).
#maximize {1,R,I : s_paths(R,I)}.



