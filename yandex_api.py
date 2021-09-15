import logging
from getpass import getpass
from yandex_music import Client

def login(token=None):
    if token != None:
        client = Client.from_token(token)
    else:
        email = input('email: ')
        password = getpass('password: ')
        client = Client.from_credentials(email,password)
        print(client.token)
    return client

def get_track_list_yandex(token=None):
    logging.basicConfig(level=logging.CRITICAL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    print(token)
    client = login(token)
    tracks = client.users_playlists(3).tracks
    print(f'Total tracks in yandex ',len(tracks))
    short_tracks = []
    for track in tracks:
        artists = " ".join(track.track.artists_name()[:2])
        short_tracks.append(f'{artists}' + ' ' + f'{track.track.title}')

    return short_tracks