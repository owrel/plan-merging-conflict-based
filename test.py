from wrapper import read, base_ipf, global_heatmap, solver, pe_single_heatmap_value, pretty_file_name, pe_simple_threshold, select_portion_based_on_heatmap
# from wrapper.pathselection import pe_single_heatmap_value




instance = read('test_instances/instance08.lp')

r, s = base_ipf(instance, npaths=10, additional_paths_computation=False, horizon_modifier=2)


ih, gh, lgh, stats = global_heatmap(r + instance)

print(stats)

# print(lgh)

r,s = select_portion_based_on_heatmap(stats.additional_data['summed_heatmap_per_path'])

print(r)
print(s)


# print(r)

# print(instance + r)

# for i in range(3):
#     ih, gh, stats = global_heatmap(r + instance)



#     # print(ih[0:10])
#     # print()
#     # print(gh[0:10])



#     cva =  pe_single_heatmap_value(ih,gh)

#     r,s = solver(cva + r + instance, encoding='pathelimination/path_elimination.lp' )

#     r,s = solver(r, 'pathelimination/convert_to_kill.lp')

#     print(r,s)


# r,s = solver(r, 'pathselection/conflict_based.lp', parameters=['0','--opt-strategy=usc'])

# print(r)