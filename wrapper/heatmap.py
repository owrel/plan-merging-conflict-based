from .helper import Stats

import clingo
import time



class OnModelIndividualHeatmap:
    def __init__(self, nagents) -> None:
        self.individual_heatmap = []
        self.global_heatmap = dict()
        self.nagents = nagents
        self.summed_heatmap_per_path = {}

    def __call__(self, cmodel: clingo.Model):
        symbols = cmodel.symbols(shown=True)
        mem = {}
        for symbol in symbols:
            if symbol.name == "individual_heatmap":
                R = symbol.arguments[0].number
                V = (symbol.arguments[1].arguments[0].number,
                     symbol.arguments[1].arguments[1].number)
                T = symbol.arguments[2].number
                K = symbol.arguments[3].arguments[0].number
                N = symbol.arguments[3].arguments[1].number

                self.individual_heatmap.append(
                    (R, V, T, int(K)/int(N))
                )

                if (V, T) in self.global_heatmap:
                    self.global_heatmap[
                        (V, T)] += (int(K)/int(N)) / self.nagents
                else:
                    self.global_heatmap[
                        (V, T)] = (int(K)/int(N)) / self.nagents
   
            if symbol.name == "at":

                R = symbol.arguments[0].number
                I = symbol.arguments[1].number
                
                V = (symbol.arguments[2].arguments[0].number,
                     symbol.arguments[2].arguments[1].number)
                T = symbol.arguments[3].number
                
                self.summed_heatmap_per_path[(R,I)] = 0
                if (R,I) in mem:
                    mem[(R,I)].append((V,T))
                else:
                    mem[(R,I)] = [(V,T)]
        
        for k in mem:
            for position in mem[k]:
                self.summed_heatmap_per_path[k] += self.global_heatmap[position]
        



def global_heatmap(
        instance: str,
        encoding: str = 'heatmap/individual_heatmap.lp'):
    now = time.time()
    ctl = clingo.Control('1')
    ctl.add(instance)
    ctl.load(encoding)

    ctl.ground([("base", [])])

    nagents = len(
        [agent for agent in ctl.symbolic_atoms.by_signature("agent", 1)])

    om = OnModelIndividualHeatmap(nagents)
    ctl.solve(on_model=om, on_finish=print)


    gh = sorted(om.global_heatmap.items(),
                key=lambda x: (x[1], x[0][1]), reverse=True)
    
    ih = sorted(om.individual_heatmap, key=lambda x: (x[3], x[0]), )

    dlgh = {}

    for k in om.summed_heatmap_per_path:
        s,a, i = min((om.summed_heatmap_per_path[a],a, i) for (i, a) in enumerate([summed_heatmap for summed_heatmap in om.summed_heatmap_per_path]) if a[0] == k[0])
        dlgh[k[0]] = a +(s,)
    
    lgh = {'pwlsh':""}
    for k in dlgh:
        lgh['pwlsh'] += f"path_with_lowest_summed_heatmap({dlgh[k][0]},{dlgh[k][1]}).\n"
        
    stats = Stats()
    lgh['summed_heatmap_per_path'] = om.summed_heatmap_per_path
    stats.total_time = time.time() - now
    return ih, gh, lgh, stats



