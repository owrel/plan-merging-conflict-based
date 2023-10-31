#defined path_killed/2.

individual_heatmap(R,V,T,(K,N)) :- 
        K = #count{1,I : at(R,I,V,T), not path_killed(R,I)}, 
        N = #count{1,I : at(R,I,_,_)}, 
        at(R,_,V,T). 






