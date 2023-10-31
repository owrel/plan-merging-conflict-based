import clingo
import random



__seed = random.randint(1, 10000)


def pretty_num(num):
    snum = str(num)
    if "e-" in snum:
        return "> 0.0"
    if "." in snum:
        return snum[: snum.index(".") + 5]
    else:
        return snum


def read(path: str) -> str:
    with open(path, "r") as file:
        encoding = file.read()

    return encoding

def pretty_file_name(path:str):
    
    slash_pos = 0
    dot_pos = len(path)
    if '/' in path:
        slash_pos = path.rindex('/')+1
    if '.' in path:
        dot_pos = path.rindex('.') 
    return path[slash_pos:dot_pos]

class Stats:
    def __init__(self, ctl: clingo.Control = None) -> None:
        self.total_time = 0
        self.solve_time = 0
        self.atoms = 0
        self.rules = 0
        self.nmodels = 0
        self.cpu = 0
        self.additional_data = {}

        if ctl:
            self.__call__(ctl)

    def merge(self, result: "Stats"):
        self.total_time += result.total_time
        self.solve_time += result.solve_time
        self.nmodels += result.nmodels
        self.atoms += result.atoms
        self.rules += result.rules
        self.cpu += result.cpu

    def __call__(self, ctl: clingo.Control):
        self.total_time += ctl.statistics["summary"]["times"]["total"]
        self.solve_time += ctl.statistics["summary"]["times"]["solve"]
        self.cpu += ctl.statistics["summary"]["times"]["cpu"]
        self.nmodels += ctl.statistics["summary"]["models"]["enumerated"]

        self.atoms += ctl.statistics["problem"]["lp"]["atoms"]
        self.rules += ctl.statistics["problem"]["lp"]["rules"]

    def __str__(self) -> str:
        ret = "Statistics\n"
        ret += f"Computed {self.nmodels} models(s)\n"
        ret += f"Grounding: {pretty_num(self.total_time-self.solve_time)} sec(s)\n"
        ret += f"Solving: {pretty_num(self.solve_time)} sec(s)\n"
        ret += f"Cpu: {pretty_num(self.cpu)} sec(s)\n"

        ret += f"Total: {pretty_num(self.total_time)} sec(s)\n"
        ret += f"Atom(s): {self.atoms}\n"
        ret += f"Rule(s): {self.rules}\n"
        return ret

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self):
        return {
            "total_time": self.total_time,
            "solving_time": self.solve_time,
            "cpu": self.cpu,
            "grounding_time": self.total_time - self.cpu,
            "nmodels": self.nmodels,
            "atoms": self.atoms,
            "rules": self.rules,
        }



class OnModel:
    def __init__(self) -> None:
        self.ret = ""

    def __call__(self, cmodel: clingo.Model):
        symbols = cmodel.symbols(shown=True)
        for symbol in symbols:
            self.ret += f"{symbol}.\n"


class OnFinish:
    def __init__(self) -> None:
        self.sat = None

    def __call__(self, solve_result: clingo.SolveResult):
        self.sat = solve_result.satisfiable


            
            
def solver(
        instance: str,
        encoding: str,
        additional_encodings: list[str] = [],
        parameters: list[str] = ['1']):

    ctl = clingo.Control(parameters)
    stats = Stats()

    ctl.load(encoding)
    for additional_encoding in additional_encodings:
        ctl.load(additional_encoding)

    ctl.add(instance)
    print('Grounding...')
    ctl.ground([("base", [])])
    print('Solving...')
    om = OnModel()
    of = OnFinish()

    ctl.solve(on_model=om,
              on_finish=of)
    stats(ctl)
    print('Done')
    print(f'Solver is {of.sat}')
    return om.ret, stats