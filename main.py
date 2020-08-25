#main file 

# todo
# - change algorithm to A* for speed
# - move reference specification out of local_price into main
# - write results to a file
# - read specifictaions from a file

import pathfinding
import read_hxm
import local_price

graph = read_hxm.makeGraph("Antarctica 24 mi.hxm")#("testmap2.hxm")
markets = ['00.01', '17.03', '43.11', '38.23', '05.13',
        '01.19', '13.19', '25.19'
    ]
paths = []
distances = []

for begin in range(len(markets)):
    #print('tic')
    placeholder_distance = []
    placeholder_paths = []
    for end in range(len(markets)):
        #print('toc')
        if begin == end:
            placeholder_distance.append(1)
            placeholder_paths.append(markets[begin])
        else:
            a, b = pathfinding.Dijkstra(graph,markets[begin],markets[end]) 
            placeholder_distance.append(a), placeholder_paths.append(b)
            
    distances.append(placeholder_distance)
    paths.append(placeholder_paths)
    
local_price.prices(markets, distances)


