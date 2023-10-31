#const portion= 80.



{ to_kill(R,I,O) : ordered_summed_heatmap_path(R,I,O)}=K/2:- npaths(K).


#maximize {O:to_kill(R,I,O)}.

#show to_kill/3.

