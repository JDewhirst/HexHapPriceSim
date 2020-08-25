#Implementation of Tao of DnD's trading system
    
#The program picks the market. It takes in the 

#print('This program calculates the prices of resources')


import copy

def prices(markets, marketDistances):
    #calculates local value of gold
    def goldPrice(localReferences):
        #localValue= 1.2
        localAvailability = localReferences / globalGoldReferences * globalGoldProduction
        #print('localAvailability', localAvailability)
        worldValue = globalGoldProduction #for gold only
        #print('worldValue', worldValue)
        localValue = localAvailability #for gold only
        #print('localValue', localValue)
        unitPerLocalAvailability = localValue/localAvailability
        #print('unitPerLocalAvailability', unitPerLocalAvailability)
        adjustmentForRarity = (globalGoldReferences/localReferences)*0.02 + 1
        #print( 'AdjForRare',adjustmentForRarity)
        cpPerUnit = unitPerLocalAvailability*adjustmentForRarity*3.125*100#8.715*240
        #print('Gold in cpPerOz = ', self.cpPerUnit)
        return cpPerUnit
            
    #calculates the value of undeveloped good in this market
    def UndevelopedGood(localReferences, globalReferences, localGoldPrice):
        localAvailability = localReferences / globalReferences * globalClayProduction
        #print('localAvailability', localAvailability)
        worldValue = globalReferences*localGoldPrice
        #print('worldValue', worldValue)
        localValue = localReferences / globalClayReferences  * worldValue
        #print('localValue', localValue)
        unitPerLocalAvailability = localValue/localAvailability
        #print('unitPerLocalAvailability', unitPerLocalAvailability)
        adjustmentForRarity = (globalClayReferences/localReferences)*0.002 + 1
        #print( 'AdjForRare',adjustmentForRarity)
        cpPerUnit = unitPerLocalAvailability*adjustmentForRarity*3.125*100 #8.715*240
        #print('Clay in cpPerUnit = ', cpPerUnit)
        return cpPerUnit
        
    def pottery(localReferences, localClayPrice): #change this to generic Manufactured Good ?
                                                  #insert local reference, and input costs
        cpPerUnit = (1+1/localReferences)*localClayPrice
        return cpPerUnit

    units  = {
        "gold": "oz.",
        "clay": "lb.",
        "pottery": "lb."
    }

    distances = marketDistances#[[1, 3, 8, 7], [3, 1, 6, 4], [8, 6, 1, 10], [7, 4, 10, 1]]
    #'00.01', '17.03', '43.11', '38.23', '05.13',
    #    '01.19', '13.19', '25.19'
    numMarkets = len(marketDistances)
    referencesGold = [1,0,0,0,0,0.2,0,0]
    referencesClay = [0,1,1,0,1,0,0.2,0]
    referencesPottery = [0,0,0,1,1,0,0.2,0]
        
    globalGoldReferences = sum(referencesGold)
    globalGoldProduction = globalGoldReferences*1320 #1320 is 1 ref in oz.

    globalClayReferences = sum(referencesClay)
    globalClayProduction = globalClayReferences*20000*16
    ### Calculates final references from the local references

    #to calculate final amount of references I need to take the local reference
    #at every market and divide it by the distance from that market to this one
    #and sum them
    goldFinal = []
    clayFinal = []
    potteryFinal = []
    for i in range(numMarkets):
        #gold
        tempGold = 0
        tempClay = 0
        tempPottery = 0
        for j in range(numMarkets):
            tempGold += referencesGold[j]/distances[i][j]
            tempClay += referencesClay[j]/distances[i][j]
            tempPottery += referencesPottery[j]/distances[i][j]
        goldFinal.append(tempGold)
        clayFinal.append(tempClay)
        potteryFinal.append(tempPottery)
    ####   
            
    # print(goldFinal)
    # print(clayFinal)
    # print(potteryFinal)

    for k in range(numMarkets):
        priceGold = goldPrice(goldFinal[k])
        priceClay = UndevelopedGood(clayFinal[k], globalClayReferences, priceGold)
        pricePottery = pottery(potteryFinal[k], priceClay)
        #pottery
        print('Price of Gold at ', markets[k], ' = ', priceGold, 'per', units.get('gold'))
        print('Price of Clay at ', markets[k], ' = ', priceClay, 'per', units.get('clay'))
        print('Price of Pottery at ', markets[k], ' = ', pricePottery, 'per', units.get('pottery'))
        
        
    # market = Market()
    # market.gold = goldPrice(1.2)
    # print(market.gold)
    # market.clay = UndevelopedGood(1, globalClayReferences, market.gold)
    # print(market.clay)
    #print(gold1.GoldValue)

