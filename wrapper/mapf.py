
from .helper import clingo, OnModel, OnFinish, __seed, Stats

import re 
def mapf(
        instance: str,
        horizon: int = 15,
        npaths: int = 5,
        encoding: str = "mapf/base_mapf.lp",
        additional_encodings: list[str] = []):
    
    rx = re.search(r"makespan\(([0-9]+)\)\.", instance)

    if rx:
        horizon = int(rx.group(1))

    ctl = clingo.Control(
        ["1", f"-c horizon={horizon}",
            f"-c npaths={npaths}", f"--seed={__seed}"]
    )

    ctl.load(encoding)

    for additional_encoding in additional_encodings:
        ctl.load(additional_encoding)

    ctl.add(instance)
    print("Grounding...")
    ctl.ground([("base", [])])

    print("Solving...")
    om = OnModel()
    of = OnFinish()

    ctl.solve(on_model=om, on_finish=of)
    s =Stats(ctl)
    s.additional_data = {'horizon':horizon}
    return om.ret, s



class OnModelPartialSolving:
    def __init__(self) -> None:
        self.ret = ""
        self.gr = 0
        self.nagent = 0

    def __call__(self, cmodel: clingo.Model):
        symbols = cmodel.symbols(shown=True)
        self.gr = 0
        self.nagent=0
        self.ret = ""
        for symbol in symbols:
            if symbol.name == "goal_reached":
                self.gr += 1
            if symbol.name == "agent":
                self.nagent += 1
            self.ret += f'{symbol}.\n'
            

def partial_solving(
        instance: str,
        encoding: str = 'mapf/partial_solving.lp',
        subgraph: str = 'mapf/subgraph.lp',
        precomputed_path: str = 'mapf/precomputed_path.lp',
        horizon:int = 15,
        horizon_modifier:int=0):

    
    rx = re.search(r"makespan\(([0-9]+)\)\.", instance)

    if rx:
        horizon = int(rx.group(1))
    
    ctl = clingo.Control(['0', f"-c horizon={horizon+horizon_modifier}", '--opt-strategy=usc' ])
    stats = Stats()

    ctl.load(encoding)
    
    
    if subgraph:
        ctl.load(subgraph)
        
    if precomputed_path:
        ctl.load(precomputed_path)

    ctl.add(instance)
    print('Grounding...')
    ctl.ground([("base", [])])
    print('Solving...')
    om = OnModelPartialSolving()
    of = OnFinish()

    ctl.solve(on_model=om,
              on_finish=of)
    stats(ctl)
    print('Done')
    print(f'Solver is {of.sat}')
    
    
    stats.additional_data = {
        'horizon' : horizon + horizon_modifier,
        'ngoal_reached' : om.gr,
        'subgraph' : subgraph,
        'precomputed_path' : precomputed_path,
        'nagent' : om.nagent
        
    }
    
    return om.ret, stats