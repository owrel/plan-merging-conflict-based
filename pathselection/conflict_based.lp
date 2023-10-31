#const n_to_kill = 5.

to_determine(R,I) :- at(R,I,_,_), not path_killed(R,I).

potential_conflict(R,I,V,T) :-
    to_determine(R,I), at(R,I,V,T), 
    to_determine(R',I'), at(R',I',V,T), 
    R'!=R.

path_composition(R,I,C) :- C = #count{1,V,T : potential_conflict(R,I,V,T)}, to_determine(R,I).


{to_kill(R,I,C): path_composition(R,I,C)} = n_to_kill.

#maximize {C:to_kill(_,_,C)}.



