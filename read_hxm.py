#this reads hexographer .hxm files to create a graph of the terrain
#which I can then feed to a pathfinding algo
    
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

    def hexString(X, Y):
    #return a string such that if x = 110 and y = 0, we get 110.00
        return f'{X:02d}'+'.'+f'{Y:02d}'

    def addNode(target, thisHex, node):
        if hexes[target]['river'] and hexes[thisHex]['river']:
            node[target] = hexes[target]['time']/2
        elif not hexes[target]['river'] and hexes[thisHex]['river']:
            node[target] = hexes[target]['time'] + 1
        else:
            node[target] = hexes[target]['time']
        
        #print(thisHex, node)

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
    #hexes = { hex : {'time':travelTime, 'river': True/False} }
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
            x_coord = (x_val - 150)//225
            if x_coord%2 == 0:
                y_coord = (y_val)//300
            else:
                y_coord = (y_val - 150)//300
            hexes[hexString(x_coord, y_coord)]['river'] = True
            
        river = inputFile.readline().split('\t')
        
    #print(hexes)
    inputFile.close()

    ###construct a dict representing graph connections###

    #first hex is bespoke, only two connections
    thisNode = {}
    hexValue = hexString(0,0)
    addNode(hexString(0,1), hexValue, thisNode)
    addNode(hexString(1,0), hexValue, thisNode)
    
    graph[hexValue] = thisNode

    #first column x= 0, y = 1:19
    for y_val in range(1,y_init):
        hexValue = hexString(0,y_val)
        thisNode = {}
        addNode(hexString(0,y_val-1), hexValue, thisNode)
        addNode(hexString(1,y_val-1), hexValue, thisNode)
        addNode(hexString(1,y_val), hexValue, thisNode)

        graph[hexValue] = thisNode
        
    #first row  x=1:18, y=0
    for x_val in range(1,x_init-1,2):
        hexValue = hexString(x_val,0)
        thisNode = {}
        addNode(hexString(x_val-1,0), hexValue, thisNode)
        addNode(hexString(x_val-1,1), hexValue, thisNode)
        addNode(hexString(x_val,1), hexValue, thisNode)
        addNode(hexString(x_val+1,0), hexValue, thisNode)
        addNode(hexString(x_val+1,1), hexValue, thisNode)
        
        graph[hexValue] = thisNode
        
    #final hex of row
    thisNode = {}
    hexValue = hexString(x,0)
    addNode(hexString(x-1,0), hexValue, thisNode)
    addNode(hexString(x,1), hexValue, thisNode)
    graph[hexValue] = thisNode

    for x_val in range(2,x_init-1,2):
        hexValue = hexString(x_val,0)
        thisNode = {}
        addNode(hexString(x_val-1,0), hexValue, thisNode)
        addNode(hexString(x_val,1), hexValue, thisNode)
        addNode(hexString(x_val+1,0), hexValue, thisNode)
                
        graph[hexValue] = thisNode
        
    #last column  x , y = 1:y-1
    thisNode = {}
    hexValue = hexString(x,y)
    addNode(hexString(x-1,0), hexValue, thisNode)
    
    graph[hexValue] = thisNode
                                
    for y_val in range(1,y_init-1):
        hexValue = hexString(x,y_val)
        thisNode = {}
        addNode(hexString(x-1,y_val), hexValue, thisNode)
        addNode(hexString(x-1,y_val-1), hexValue, thisNode)
        addNode(hexString(x,y_val-1), hexValue, thisNode)
                
        graph[hexValue] = thisNode
        
    #last row xval=1:x-1, yval = y
    for x_val in range(1,x_init-1,2):
        hexValue = hexString(x_val,y)
        thisNode = {}
        addNode(hexString(x_val-1,y), hexValue, thisNode)
        addNode(hexString(x_val,y-1), hexValue, thisNode)
        addNode(hexString(x_val+1,y), hexValue, thisNode)
                
        graph[hexValue] = thisNode
        
    for x_val in range(2,x_init-1,2):
        hexValue = hexString(x_val,y)
        thisNode = {}
        addNode(hexString(x_val-1,y), hexValue, thisNode)
        addNode(hexString(x_val-1,y-1), hexValue, thisNode)
        addNode(hexString(x_val,y-1), hexValue, thisNode)
        addNode(hexString(x_val+1,y-1), hexValue, thisNode)
        addNode(hexString(x_val+1,y), hexValue, thisNode)
                
        graph[hexValue] = thisNode

    #last hex, max of x and y is bespoke
    thisNode = {}
    hexValue = hexString(x,y)
    addNode(hexString(x-1,y-1), hexValue, thisNode)
    addNode(hexString(x-1,y), hexValue, thisNode)
    addNode(hexString(x,y-1), hexValue, thisNode)
    
    graph[hexValue] = thisNode

    ###the main body, x =1:18, y=1:18
    ##odd columns
    for x_val in range(1,x_init-1,2):
        for y_val in range(1,y_init-1):
            hexValue =  hexString(x_val,y_val)
            thisNode = {}
            addNode(hexString(x_val-1,y_val), hexValue, thisNode)
            addNode(hexString(x_val-1,y_val+1), hexValue, thisNode)
            addNode(hexString(x_val,y_val-1), hexValue, thisNode)
            addNode(hexString(x_val,y_val+1), hexValue, thisNode)
            addNode(hexString(x_val+1,y_val), hexValue, thisNode)
            addNode(hexString(x_val+1,y_val+1), hexValue, thisNode)
            
            graph[hexValue] = thisNode
            
    ##even columns
    for x_val in range(2,x_init-1,2):
        for y_val in range(1,y_init-1):
            hexValue =  hexString(x_val,y_val)
            #print(hexValue)
            thisNode = {}
            addNode(hexString(x_val-1,y_val-1), hexValue, thisNode)
            addNode(hexString(x_val-1,y_val), hexValue, thisNode)
            addNode(hexString(x_val,y_val-1), hexValue, thisNode)
            addNode(hexString(x_val,y_val+1), hexValue, thisNode)
            addNode(hexString(x_val+1,y_val-1), hexValue, thisNode)
            addNode(hexString(x_val+1,y_val), hexValue, thisNode)
        
            graph[hexValue] = thisNode
            
    
    return(graph)

# graph = makeGraph("testmap.hxm")
# print(graph['02.03'])

    
    
