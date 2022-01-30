import requests


class SpotifyApi:

    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    API_URL = 'https://api.spotify.com/v1'

    def __init__(self, client_id, client_secret, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.client_id = client_id
        self.client_secret = client_secret

        self.token_type = None
        self.access_token = None

    def get_client_credentials(self):

        from base64 import b64encode

        client_creds = f'{self.client_id}:{self.client_secret}'
        client_creds_b64 = b64encode(client_creds.encode())

        return client_creds_b64.decode()

    def get_token_headers(self):

        return {
            'Authorization': f'Basic {self.get_client_credentials()}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

    def get_token_data(self, code, redirect_uri):

        return {
            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }

    def build_auth_url(self, redirect_uri):
        from random import choices
        from string import ascii_letters, digits

        state = "".join(choices(ascii_letters + digits, k=16))
        scope = "user-read-private user-read-email"

        return "https://accounts.spotify.com/authorize?" + "response_type=code" + f"&client_id={self.client_id}" + f"&scope={scope}" + \
            f"&redirect_uri={redirect_uri}" + f"&state={state}"

    def get_access_token_json(self, code, redirect_uri):

        r = requests.post(self.TOKEN_URL, data=self.get_token_data(
            code, redirect_uri), headers=self.get_token_headers())

        if r.ok:
            return r.json()

        raise Exception(r.text)

    def get_my_playlists(self):
        r = requests.get(self.API_URL + '/me/playlists', headers={'Authorization': f'{self.token_type} {self.access_token}',
                                                                                   'Content-Type': 'application/json',
                                                                                   'Host': 'api.spotify.com'})

        if r.ok:
            return r.json()

        raise Exception(r.text)

    def get_playlist_by_id(self, playlist_id):
        r = requests.get(self.API_URL + '/playlists/' + playlist_id, headers={'Authorization': f'{self.token_type} {self.access_token}',
                                                                              'Content-Type': 'application/json',
                                                                              'Host': 'api.spotify.com'})
        if r.ok:
            return r.json()

        raise Exception(r.text)

    def get_tracks_features(self, ids):
        r = requests.get(self.API_URL + f'/audio-features?ids={ids}', headers={'Authorization': f'{self.token_type} {self.access_token}',
                                                                               'Content-Type': 'application/json',
                                                                               'Host': 'api.spotify.com'})
        if r.ok:
            return r.json()['audio_features']

        raise Exception(r.text)

    def get_recommendations(self, query):

        r = requests.get(
            self.API_URL + '/recommendations', params=query, headers={'Authorization': f'{self.token_type} {self.access_token}',
                                                                      'Content-Type': 'application/json',
                                                                      'Host': 'api.spotify.com'})

        if r.ok:
            return r.json()

        raise Exception(r.text)
