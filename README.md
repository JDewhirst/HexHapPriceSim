# HexMapPriceSim
Local Price Calculations on RPG Hex Map

This set of scripts is takes in a stored hex map, produced in the software hexographer (https://www.hexographer.com/), the coordinates of 'markets' on that map, and the relative abundance of various goods (limited at the moment to gold, clay, and pottery), which it uses to calculate the price of those goods at each market.

read.hxm reads in from a .hxm file used by hexographer, creating a representation of the map as a graph.

Pathfinding.py contains an implementation of djikstras algorithm which is used to calculate the shortest distance between two markets.

Provided with the distances between the markets and the relative abundance of resources at those markets local_price.py will calculate the price of goods at each market.

