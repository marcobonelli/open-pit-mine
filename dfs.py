graph1 = {  0 : [1],
            1 : [0, 2, 3, 5],    # edit: corrected from [0, 2] to [0, 2, 3, 5]
            2 : [1],
            3 : [1, 4],
            4 : [3, 5],
            5 : [1, 4] }

# graph1 = { 0 : [1],
#            1 : [0],
#            2 : [3, 4],
#            3 : [2, 4],
#            4 : [2, 3] }

# graph1 = { 0 : [],
#            1 : [],
#            2 : [3, 4],
#            3 : [2],
#            4 : [2] }


def cycle_exists(G):                      # - G is an undirected graph.              
    marked = { u : False for u in G }     # - All nodes are initially unmarked.
    found_cycle = [False]                 # - Define found_cycle as a list so we can change
                                          # its value per reference, see:
                                          # http://stackoverflow.com/questions/11222440/python-variable-reference-assignment
    for u in G:                           # - Visit all nodes.
        if not marked[u]:
            dfs_visit(G, u, found_cycle, u, marked)     # - u is its own predecessor initially
        if found_cycle[0]:
            break
    return found_cycle[0]
 
#--------
caminho = []
def dfs_visit(G, u, found_cycle, pred_node, marked):
    if found_cycle[0]:                                # - Stop dfs if cycle is found.
        return
    marked[u] = True                                  # - Mark node.
    for v in G[u]:                                    # - Check neighbors, where G[u] is the adjacency list of u.
        if marked[v] and v != pred_node:              # - If neighbor is marked and not predecessor,
            found_cycle[0] = True                     # then a cycle exists.
            return
        if not marked[v]:                             # - Call dfs_visit recursively.
            dfs_visit(G, v, found_cycle, u, marked)
            if(found_cycle == [True]):
                caminho.append(v)

assert(cycle_exists(graph1) == True)
print("Graph1 has a cycle.")
print(caminho)