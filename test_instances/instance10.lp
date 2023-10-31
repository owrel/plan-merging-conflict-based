agent(1).
agent(2).
vertex((1,1)).
vertex((2,1)).
vertex((3,1)).
vertex((4,1)).
vertex((5,1)).
vertex((3,2)).
edge((2,1),(1,1)).
edge((3,1),(2,1)).
edge((4,1),(3,1)).
edge((5,1),(4,1)).
edge((3,2),(3,1)).
edge((3,1),(3,2)).
edge((1,1),(2,1)).
edge((2,1),(3,1)).
edge((3,1),(4,1)).
edge((4,1),(5,1)).
goal(1,(5,1)).
goal(2,(1,1)).
start(1,(2,1)).
start(2,(4,1)).


horizon(1,3).
horizon(2,3).

makespan(30).