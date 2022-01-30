import pandas as pd


class TracksAnalyzer:

    def __init__(self, json_data):
        self.data = pd.json_normalize(json_data)

    def analyze(self):
        pass
