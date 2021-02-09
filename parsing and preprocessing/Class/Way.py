from haversine import haversine, Unit


class Way:
    def __init__(self):
        self.nodes = []
        self.simple_way = []
        self.simple_nodes = []
        self.length = []
        self.location = {'coordinates': [],
                         'type': 'LineString'}

    def set_location(self, nodes):
        self.location['coordinates'] = nodes

    def len(self, nodes):
        j = 0
        self.length = [0] * (len(self.simple_way) - 1)
        for i in range(len(self.length)):
            self.simple_nodes.append([])
            while self.nodes[j] != self.simple_way[i + 1]:
                self.simple_nodes[i].append([self.location['coordinates'][j][1], self.location['coordinates'][j][0]])
                self.length[i] += haversine((self.location['coordinates'][j][1],
                                             self.location['coordinates'][j][0]),
                                            (self.location['coordinates'][j + 1][1],
                                             self.location['coordinates'][j + 1][0]), Unit.METERS)
                j += 1
            self.simple_nodes[i].append([self.location['coordinates'][j][1], self.location['coordinates'][j][0]])
