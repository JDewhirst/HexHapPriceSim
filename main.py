#main file 

# todo
# - change algorithm to A* for speed
# - move reference specification out of local_price into main
# - write results to a file
# - read specifictaions from a file

import pathfinding
import read_hxm
import local_price

graph = read_hxm.makeGraph("testmap.hxm")#("testmap2.hxm")
#print(graph)
markets = ['00.01', '05.05', '08.08'
    ]
paths = []
distances = []

for begin in range(len(markets)):
    placeholder_distance = []
    placeholder_paths = []
    for end in range(len(markets)):
        try:
            #if distance end->begin already calced, just sub it in
            #same for path
            if distances[begin][end]:
                placeholder_distance.append(distances[begin][end])
                placeholder_paths.append(reverse(paths[begin][end]))
        except:
             if begin == end:
                 placeholder_distance.append(1)
                 placeholder_paths.append(markets[begin])
             else:
                 a, b = pathfinding.Dijkstra(graph,markets[begin],markets[end]) 
                 placeholder_distance.append(a), placeholder_paths.append(b)
            
    distances.append(placeholder_distance)
    paths.append(placeholder_paths)

references = [ [1,0,0], [0,1,1], [0.1,0,0] ]
#references [ [gold], [clay], [pottery]]
local_price.prices(markets, distances, references)#markets, distances, references


