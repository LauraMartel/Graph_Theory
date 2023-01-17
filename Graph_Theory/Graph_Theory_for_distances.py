# This code was written with the help of chatgPT

from math import radians, sin, cos, sqrt, atan, pi, tan, atan2
from coordinates import coord
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm


import random
class CityDistance:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def distance(self, city1, city2):
        """
        Calculate the precise distance between two cities on Earth in kilometers using Vincenty's formula.
        """
        lat1, lon1 = radians(self.coordinates[city1][0]), radians(self.coordinates[city1][1])
        lat2, lon2 = radians(self.coordinates[city2][0]), radians(self.coordinates[city2][1])
        # WGS-84 Earth's mean radius in meters
        a = 6378137
        b = 6356752.314245
        f = 1 / 298.257223563
        L = lon2 - lon1
        U1 = atan((1 - f) * tan(lat1))
        U2 = atan((1 - f) * tan(lat2))
        sinU1, cosU1 = sin(U1), cos(U1)
        sinU2, cosU2 = sin(U2), cos(U2)
        lambdaL = L
        lambdaP = 2 * pi
        iterLimit = 20
        while abs(lambdaL - lambdaP) > 1e-12 and iterLimit > 0:
            sinLambda = sin(lambdaL)
            cosLambda = cos(lambdaL)
            sinSigma = sqrt((cosU2 * sinLambda) ** 2 + (cosU1 * sinU2 - sinU1 * cosU2 * cosLambda) ** 2)
            if sinSigma == 0:
                return 0  # co-incident points
            cosSigma = sinU1 * sinU2 + cosU1 * cosU2 * cosLambda
            sigma = atan2(sinSigma, cosSigma)
            sinAlpha = cosU1 * cosU2 * sinLambda / sinSigma
            cosSqAlpha = 1 - sinAlpha ** 2
            cos2SigmaM = cosSigma - 2 * sinU1 * sinU2 / cosSqAlpha
            C = f / 16 * cosSqAlpha * (4 + f * (4 - 3 * cosSqAlpha))
            lambdaP = lambdaL
            lambdaL = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2SigmaM + C * cosSigma * (-1 + 2 * cos2SigmaM)))
            uSq = cosSqAlpha * (a * a - b * b) / (b * b)
            A = 1 + uSq / 16384 * (4096 + uSq * (-768 + uSq * (320 - 175 * uSq)))
            B = uSq / 1024 * (256 + uSq * (-128 + uSq * (74 - 47 * uSq)))
            deltaSigma = B * sinSigma * (cos2SigmaM + B / 4 * (cosSigma * (-1 + 2 * cos2SigmaM * cos2SigmaM) - B / 6 * cos2SigmaM * (-3 + 4 * sinSigma * sinSigma) * (-3 + 4 * cos2SigmaM * cos2SigmaM)))
            distance_km = b * A * (sigma - deltaSigma)
        return (city1, city2, distance_km / 1000)

    # function to create a list of dictionaries containing two cities randomly picked and their distance.
    # The function should pick several times a city as city1 to later be relevant for graph theory
    def random_cities(self,n):
        keys = list(self.coordinates.keys())
        city_list = []
        if n>len(keys):
            n = len(keys)
        while len(city_list) < n:
            city1 = random.choice(keys)
            city2 = random.choice(keys)
            while city2 == city1:
                city2 = random.choice(keys)
            city_list.append(self.distance(city1,city2))
        return city_list

    # create a directed graph and add nodes and edges
    def create_graph(self,n):
        city_list = self.random_cities(n)
        G = nx.DiGraph()
        for city in self.coordinates.keys():
            G.add_node(city)
        for city1,city2,distance in city_list:
            G.add_edge(city1,city2, weight=distance)
        return G

    # Plot the graph from the create_graph function.
    # I prefered to display it using circular layout as it seemed clearer.
    def plot_graph(self, n):
        G = self.create_graph(n)
        pos = nx.circular_layout(G)
        # pos = nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G, pos, node_size=700)
        edges = G.edges()
        weights = [G[u][v]['weight'] for u,v in edges]
        widths = [0.1 + (G[u][v]['weight']/max(weights))*5 for u,v in edges]
        nx.draw_networkx_edges(G, pos, width=widths, edge_color=cm.Blues(weights))
        edge_labels = {(u,v):round(d) for u,v,d in G.edges(data='weight')}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        nx.draw_networkx_labels(G, pos, font_size=10)
        plt.box(False)
        plt.show()


# Precise the number of cities
n = 30

# Call the class
cities = CityDistance(coord)

# Display the graph
cities.plot_graph(n)
