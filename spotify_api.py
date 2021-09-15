from os import access
import spotipy
from spotipy import client
from spotipy.oauth2 import SpotifyOAuth
import base64
import requests
import datetime
from urllib.parse import urlencode

client_id = '6b0b06db29a8447ea5e4aff13e2f732d'
client_secret = 'e64342d84cfd4ddc9adb9d3c02f76f35'
redirect_uri = 'http://127.0.0.1:9090'


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        if self.client_id == None or self.client_secret == None:
            raise Exception("You must set client id and client secret")
        client_id = self.client_id
        client_secret = self.client_secret
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_headers(self):
        client_creds = self.get_client_credentials()
        token_header = {
            'Authorization':  f'Basic {client_creds}'
        }
        return token_header

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_header = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_header)
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            print("Auth fail")
            return False
        response = r.json()
        now = datetime.datetime.now()
        self.access_token = response['access_token']
        expires_in = response['expires_in']
        self.access_token_expires = now + \
            datetime.timedelta(seconds=expires_in)
        self.access_token_did_expire = now < self.access_token_expires

    def auth_v2(self):
        client_id = self.client_id
        response_type = 'code'
        redirect_uri = 'http://127.0.0.1:9090'
        scope = 'user-library-modify'
        endpoint = 'https://accounts.spotify.com/authorize'
        data = urlencode({"client_id": client_id, 'response_type': response_type,
                         'redirect_uri': redirect_uri, 'scope': scope})
        auth_url = f'{endpoint}?{data}'
        r = requests.get(auth_url)
        print(r.json())


def search_tracks(list_of_tracks):
    sp = SpotifyAPI(client_id, client_secret)
    sp.auth()
    access_token = sp.access_token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    endpoint = "https://api.spotify.com/v1/search"
    for lookup_track in list_of_tracks:
        data = urlencode({"q": lookup_track, "type": "track", "limit": 1})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)
        tracks = r.json()['tracks']['items']
        if len(tracks) == 0:
            print('Track ', lookup_track, ' didnt founded')
            continue
        # for track in tracks:
        #     print('Artist info:')
        #     artists = track['artists']
        #     for artist in artists:
        #         print('Artist', artist['name'])
        #         print('Artist id', artist['id'])
        #     print('Track info:')
        #     print('Track', track['name'])
        #     print('Id', track['id'])
        #     print('-----------------------------')


def search_tracks_v2(list_of_tracks):
    scope = 'user-library-modify'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                         client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    tracks_id_list = []
    for lookup_track in list_of_tracks:
        r = sp.search(lookup_track,limit=1)
        tracks = r['tracks']['items']
        if len(tracks) == 0:
            print('Track ', lookup_track, ' didnt founded')
            continue
        for track in tracks:
            # print('Artist info:')
            # artists = track['artists']
            # for artist in artists:
            #     print('Artist', artist['name'])
            # print('Track info:')
            # print('Track', track['name'])
            # print('Id', track['id'])
            # print('-----------------------------')
            tracks_id_list.append(track['id'])
            if len(tracks_id_list) == 50:
                print('Adding set of tracks')
                sp.current_user_saved_tracks_add(tracks_id_list)
                tracks_id_list.clear()
    if len(tracks_id_list) != 0:
        print('Adding last set of tracks')
        sp.current_user_saved_tracks_add(tracks_id_list)
        tracks_id_list.clear()
    

def delete_all_saved_tracks():
    scope = 'user-library-read user-library-modify'
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                         client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))
    
    r = sp.current_user_saved_tracks(limit=2,offset=0)
    remove_id_list = []
    total_tracks = r['total']
    print('Total tracks in spotify ',total_tracks)
    deleted = 0
    while deleted < total_tracks:
        r = sp.current_user_saved_tracks(limit=50)
        items = r['items']
        for item in items:
                track = item['track']
                # print('Artist info:')
                # artists = track['artists']
                # for artist in artists:
                #     print('Artist', artist['name'])
                # print('Track info:')
                # print('Track', track['name'])
                # print('Id', track['id'])
                remove_id_list.append(track['id'])
                # print('-----------------------------')
        sp.current_user_saved_tracks_delete(remove_id_list)
        deleted += len(remove_id_list)
        remove_id_list.clear()
        
        
