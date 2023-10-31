from .helper import OnFinish, __seed, Stats

import clingo
import re
import time
from tqdm import tqdm


class UnsatIPF(Exception):
    pass


class Naive_ipf:
    def __init__(self) -> None:
        self.ret = ""

    def __call__(self, cmodel: clingo.Model) -> any:
        symbols = cmodel.symbols(shown=True)
        for symbol in symbols:
            self.ret += f"{str(symbol)}.\n "


def naive_ipf(
        instance: str,
        horizon: int = 15,
        npaths: int = 5,
        encoding: str = "ipf/naive_ipf.lp",
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
    om = Naive_ipf()
    of = OnFinish()

    ctl.solve(on_model=om, on_finish=of)

    if not of.sat:
        raise UnsatIPF()

    return om.ret, Stats(ctl)


class OnModelNaiveIPF:
    def __init__(self, agent_id) -> None:
        self.agent_id = agent_id
        self.ret = ""
        self.path_id = 1

    def __call__(self, cmodel: clingo.Model):
        symbols = cmodel.symbols(shown=True)

        for symbol in symbols:
            if symbol.name == "at":
                self.ret += f"at({self.agent_id},{self.path_id},{str(symbol.arguments[0])},{str(symbol.arguments[1])}).\n"

        self.path_id += 1


def base_ipf(
        instance: str,
        horizon: int = 15,
        npaths: int = 15,
        encoding: str = "ipf/base_ipf.lp",
        use_optimization: bool = True,
        horizon_modifier: int =0,
        additional_paths_computation: bool = False,
        additional_paths_horizon_modifier: int = 2,
        additional_encodings: list[str] = []):
    rx = re.search(r"makespan\(([0-9]+)\)\.", instance)

    if rx:
        horizon = int(rx.group(1)) + horizon_modifier

    print(horizon)
    ctl = clingo.Control(
        [f"{npaths}", f"-c horizon={horizon}", f"--seed={__seed}"])

    ctl.load(encoding)

    for additional_encoding in additional_encodings:
        ctl.load(additional_encoding)

    ctl.add(instance)
    now = time.time()

    print("Grounding...")

    ctl.ground([("base", [])])

    agents = [agent for agent in ctl.symbolic_atoms.by_signature("agent", 1)]

    stats = Stats()

    ret = []
    unsat = []
    details = []
    
    for agent in (pbar := tqdm(agents)):
        agent_id = agent.symbol.arguments[0].number

        agent_horizon = horizon

        if use_optimization:
            [
                (agent_horizon := h.symbol.arguments[1].number)
                for h in ctl.symbolic_atoms.by_signature("horizon", 2)
                if agent_id == h.symbol.arguments[0].number
            ]

        if agent_horizon == horizon:
            use_optimization = False
        
        [
            (
                start_pos := clingo.Function(
                    "at", [start.symbol.arguments[1], clingo.Number(0)]
                )
            )
            for start in ctl.symbolic_atoms.by_signature("start", 2)
            if start.symbol.arguments[0].number == agent_id
        ]

        [
            (
                goal_pos := clingo.Function(
                    "at", [goal.symbol.arguments[1],
                           clingo.Number(agent_horizon+horizon_modifier)]
                )
            )
            for goal in ctl.symbolic_atoms.by_signature("goal", 2)
            if goal.symbol.arguments[0].number == agent_id
        ]

        pbar.set_description(
            f"Current agent: {agent_id} - {start_pos} => {goal_pos}")

        om = OnModelNaiveIPF(agent_id)
        of = OnFinish()
        ctl.solve(
            on_model=om, on_finish=of, assumptions=[
                (start_pos, True), (goal_pos, True)]
        )
        stats(ctl)
        ret.append(om.ret)

        if additional_paths_computation and additional_paths_horizon_modifier:
            if (agent_horizon + additional_paths_horizon_modifier) <= int(horizon):
                goal_pos = clingo.Function(
                    "at", [goal_pos.arguments[0], clingo.Number(
                        agent_horizon+horizon_modifier+additional_paths_horizon_modifier)]
                )
                pbar.set_description(
                    f"Current agent: {agent_id} - {start_pos} => {goal_pos}")

                om_additional = OnModelNaiveIPF(agent_id)
                om_additional.path_id = om.path_id

                ctl.solve(
                    on_model=om_additional, on_finish=of, assumptions=[
                        (start_pos, True), (goal_pos, True)]
                )
                stats(ctl)
                # print(Stats(ctl))
                ret.append(om_additional.ret)
    
    stats.additional_data = {
        'npaths': stats.nmodels,
        'use_optimization': use_optimization,
        'horizon_modifier': horizon_modifier ,
        'additional_paths_computation': additional_paths_computation,
        'additional_paths_horizon_modifier':  additional_paths_horizon_modifier,
        'nagent': len(agents)
    }

    return "\n" + "\n".join(ret), stats
