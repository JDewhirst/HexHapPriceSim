#this reads hexographer .hxm files to create a graph of the terrain
#which I can then feed to a pathfinding algo

def hexString(X, Y):
    #return a string such that if x = 110 and y = 0, we get 110.00
    return f'{X:02d}'+'.'+f'{Y:02d}'
    
#.hxm stores each hex as a line of tab seperated strings
#first string is the name of the terrain
#these are the travel times (in days) associated with each string
travelTimes = {'Ocean':1/3,
            'Sea':2/3,
            'Deep Sea':1,
            'Mountains':3,
            'Light Forest':2,
            'Light Evergreen':2,
            'Hills':2,
            'Grassy Hills':2,
            'Heavy Forest':3,
            'Heavy Evergreen':3,
            'Forested Mountains':4,
            'Evergreen Mountains':4,
            'Snowcapped Mountains':4,
            'Rocky Desert':2,
            'Forested Hills':3,
            'Evergreen Hills':3,
            'Sandy Desert':1,
            'Grassland':1,
            'Farmland':1,
            'Grazing Land':1,
            'Snow Fields': 2,
            'Marsh':3,
            'Evergreen Wetlands':2
            }

def makeGraph(filename):

    def addNode(X,Y, node):
        node[hexString(X,Y)] = hexes[hexString(X,Y)]['time']
        #print(node)

    inputFile = open(filename,"r", encoding='UTF-16')
    #find dimensions of the map
    firstLine = inputFile.readline().split(',')
    x_init, y_init = int(firstLine[0]), int(firstLine[1]) 
    x, y = x_init-1, y_init-1
        
    hexes_not_found = True

    #reads until beginning of hexes
    while hexes_not_found:
        line = inputFile.readline().split()
        if line[0] == 'hexes':
            hexes_not_found = False
    #print(line)

    #initialise dict of weights of hexes
    hexes = {}

    #empty graph
    graph = {}

    #store the value of each hex with its co-ords in XXYY format
    for x_val in range(x_init):
        for y_val in range(y_init):
            #each hex with a feature adds a new line describing that feature
            #any num of features will throw this off
            line = inputFile.readline().split('\t')
            #print(x_val,y_val,line[0])
            #hexValue = f'{x_val:02d}' + f'{y_val:02d}'
            hexes[hexString(x_val,y_val)] = {'time':travelTimes[line[0]],'river':False}
            
    #check if rivers are present and update 'river' entry for applicable hexes
    river = inputFile.readline().split('\t')
    while river != ['']:
        #.hxm stores each river on its own line
        for i in range(7,len(river)):
            x_val, y_val = river[i].split(',')
            x_val, y_val = int(x_val.strip('0').strip('.')), int(y_val.strip('\n').strip('0').strip('.'))
            x_coord = 1+ (x_val - 150)//225
            if x_coord%2 == 0:
                y_coord = (y_val)//300
            else:
                y_coord = 1 + (y_val - 150)//300
            #check the travel time on this hex
            #if it's > 1 subtract 1
            # if it's 1, set to 1/2
            hexes[hexString(x_coord, y_coord)]['river'] = True
            
        river = inputFile.readline().split('\t')
    inputFile.close()

    ###construct a dict representing graph connections###

    #first hex is bespoke, only two connections
    thisNode = {}
    addNode(0,1,thisNode)
    addNode(1,0,thisNode)
    
    graph[hexString(0,0)] = thisNode

    #first column x= 0, y = 1:19
    for y_val in range(1,y_init):
        hexValue = hexString(0,y_val)
        thisNode = {}
        addNode(0,y_val-1,thisNode)
        addNode(1,y_val-1,thisNode)
        addNode(1,y_val,thisNode)

        graph[hexValue] = thisNode
        
    #first row  x=1:18, y=0
    for x_val in range(1,x_init-1,2):
        hexValue = hexString(x_val,0)
        thisNode = {}
        addNode(x_val-1,0,thisNode)
        addNode(x_val-1,1,thisNode)
        addNode(x_val,1,thisNode)
        addNode(x_val+1,0,thisNode)
        addNode(x_val+1,1,thisNode)
        
        graph[hexValue] = thisNode
        
    #final hex of row
    thisNode = {}
    addNode(x-1,0,thisNode)
    addNode(x,1,thisNode)
    graph[hexString(x,0)] = thisNode

    for x_val in range(2,x_init-1,2):
        hexValue = hexString(x_val,0)
        thisNode = {}
        addNode(x_val-1,0,thisNode)
        addNode(x_val,1,thisNode)
        addNode(x_val+1,0,thisNode)
                
        graph[hexValue] = thisNode
        
    #last column  x , y = 1:y-1
    thisNode = {}
    addNode(x-1,0,thisNode)
    addNode(x-1,0,thisNode)
    addNode(x-1,0,thisNode)
    
    graph[hexString(x,y)] = thisNode
                                
    for y_val in range(1,y_init-1):
        hexValue = hexString(x,y_val)
        thisNode = {}
        addNode(x-1,y_val,thisNode)
        addNode(x-1,y_val-1,thisNode)
        addNode(x,y_val-1,thisNode)
                
        graph[hexValue] = thisNode
        
    #last row xval=1:x-1, yval = y
    for x_val in range(1,x_init-1,2):
        hexValue = hexString(x_val,y)
        thisNode = {}
        addNode(x_val-1,y,thisNode)
        addNode(x_val,y-1,thisNode)
        addNode(x_val+1,y,thisNode)
                
        graph[hexValue] = thisNode
        
    for x_val in range(2,x_init-1,2):
        hexValue = hexString(x_val,y)
        thisNode = {}
        addNode(x_val-1,y,thisNode)
        addNode(x_val-1,y-1,thisNode)
        addNode(x_val,y-1,thisNode)
        addNode(x_val+1,y-1,thisNode)
        addNode(x_val+1,y,thisNode)
                
        graph[hexValue] = thisNode

    #last hex, max of x and y is bespoke
    thisNode = {}
    addNode(x-1,y-1,thisNode)
    addNode(x-1,y,thisNode)
    addNode(x,y-1,thisNode)
    
    graph[hexString(x,y)] = thisNode

    ###the main body, x =1:18, y=1:18
    ##odd columns
    for x_val in range(1,x_init-1,2):
        for y_val in range(1,y_init-1):
            hexValue =  hexString(x_val,y_val)
            addNode(x_val-1,y_val,thisNode)
            addNode(x_val-1,y_val+1,thisNode)
            addNode(x_val,y_val-1,thisNode)
            addNode(x_val,y_val+1,thisNode)
            addNode(x_val+1,y_val,thisNode)
            addNode(x_val+1,y_val+1,thisNode)
            
            graph[hexValue] = thisNode
            
    ##even columns
    for x_val in range(2,x_init-1,2):
        for y_val in range(1,y_init-1):
            hexValue =  hexString(x_val,y_val)
            #print(hexValue)
            addNode(x_val-1,y_val-1,thisNode)
            addNode(x_val-1,y_val,thisNode)
            addNode(x_val,y_val-1,thisNode)
            addNode(x_val,y_val+1,thisNode)
            addNode(x_val+1,y_val-1,thisNode)
            addNode(x_val+1,y_val,thisNode)
        
            graph[hexValue] = thisNode
            
    
    return(graph)

# graph = makeGraph("testmap.hxm")
# print(graph['02.03'])

    
    
