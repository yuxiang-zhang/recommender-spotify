from abc import ABC, abstractmethod

import pandas as pd


class RecommendStrategy(ABC):

    @abstractmethod
    def recommend(self, data: pd.DataFrame):
        pass


class MeanRS(RecommendStrategy):

    def recommend(self, track_features: pd.DataFrame, artist_ids: str) -> dict:

        target_cols = ['acousticness', 'danceability', 'duration_ms', 'energy', 'instrumentalness',
                       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence']

        data = track_features[target_cols]

        normalized_data = (data - data.min()) / (data.max() - data.min())
        query_params = data.mean()[normalized_data.std() < 0.5].add_prefix(
            'target_').to_dict()

        for key in ('target_duration_ms', 'target_key', 'target_mode', 'target_time_signature'):
            if key in query_params:
                query_params[key] = int(query_params[key])

        query_params['seed_artists'] = artist_ids
        query_params['seed_genres'] = ''
        query_params['seed_tracks'] = ''
        query_params['limit'] = 10

        return query_params
