from .helper import solver, Stats
import time

def pe_single_heatmap_value(ih,gh):
    now = time.time()
    
    critical_vertices = [(gh[0][0][0], gh[0][0][1])]
    
    print(critical_vertices)
    
    
    intersection = set()
    
    for cv in critical_vertices:
        min_ih = (0,(0,0),0,1)
        for ih_value in ih:
            if (ih_value[1],ih_value[2]) == cv:
                # print(cv, (ih_value[1],ih_value[2]), cv == (ih_value[1],ih_value[2]))
                # print(ih_value[3], min_ih[3])
                # print(ih_value)
                if ih_value[3] <= min_ih[3]: 
                    # print('hello')
                    min_ih = ih_value
                
            # print(intersection)
        intersection.add(min_ih)
            
    
    critical_vertex_agent = "\n".join([f"critical_vertex({info[1]},{info[2]}). critical_agent({info[0]})." for info in intersection]) 
    stats = Stats()
    stats.total_time = time.time() - now
    return critical_vertex_agent, stats
    
    
def pe_simple_threshold(ih ,gh, nagent, bias=1):
    now = time.time()
    
    critical_vertices = []
    
    
    for h in gh:
        if h[1] > 1/int(nagent):
            critical_vertices.append(h[0])
    
    print(len(ih), len(critical_vertices), 1/int(nagent))
    print(critical_vertices)
    
    intersection = set()
    
    for cv in critical_vertices:
        min_ih = (0,(0,0),0,1)
        for ih_value in ih:
            if (ih_value[1],ih_value[2]) == cv:
                # print(cv, (ih_value[1],ih_value[2]), cv == (ih_value[1],ih_value[2]))
                # print(ih_value[3], min_ih[3])
                # print(ih_value)
                if ih_value[3] <= min_ih[3]: 
                    # print('hello')
                    min_ih = ih_value
                
            # print(intersection)
        intersection.add(min_ih)
            
    
    critical_vertex_agent = "\n".join([f"critical_vertex({info[1]},{info[2]}). critical_agent({info[0]},{info[1]},{info[2]})." for info in intersection]) 
    stats = Stats()
    stats.total_time = time.time() - now
    stats.additional_data = {'ncritical_vertex' : len(critical_vertices), 'bias' : bias}
    return critical_vertex_agent, stats

def select_portion_based_on_heatmap(summed_heatmap_per_path, portion=0.7):
    now = time.time()
    ret = ""
    
    for elem in sorted(summed_heatmap_per_path, key= lambda x: summed_heatmap_per_path[x], reverse=True)[:int(len(summed_heatmap_per_path)*portion)]:
        ret += f"to_kill{(elem[0],elem[1])}.\n"
    stats = Stats()
    stats.total_time = time.time() - now
    
    return ret, stats
    