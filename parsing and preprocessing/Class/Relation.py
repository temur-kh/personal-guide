class Relation:
    def __init__(self):
        self.road = None
        self.ways = []
        self.outer = []
        self.location = {'coordinates': [],
                         'type': 'MultiLineString'}

    def set_location(self, ways):
        self.location['coordinates'] = ways
