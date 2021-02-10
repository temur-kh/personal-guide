class Node:
    def __init__(self):
        self.location = {'coordinates': [],
                         'type': 'Point'}
        self.road = {
            'crossroads': False,
            'start_end': 0,
            'input': 0}
        self.save = False