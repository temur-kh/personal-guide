from data_processing.data_processor import DataProcessor


class OSMDataProcessor(DataProcessor):

    source_name = ""

    def __init__(self, source_name):
        super().__init__(source_name)

    def create_connection(self):
        pass

    def query(self, params=None):
        pass

    def close_connection(self):
        pass

