#const npath = 5.
{dpath(R,I): at(R,I,_,_)} npath :- agent(R).

#maximize {1@2,R,I : dpath(R,I)}.

dpath(R,I,V,T) :- dpath(R,I), at(R,I,V,T).

#maximize {1@1R,V,T : dpath(_,_,V,T)}.