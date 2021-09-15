from yandex_api import *
from spotify_api import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth


if __name__ == '__main__':
    yandex_tracks = get_track_list_yandex(token="AQAAAAAJ5tsaAAG8XhYX38JR9kNJigno9RhtHGs")
    delete_all_saved_tracks()
    search_tracks_v2(yandex_tracks)
    print('Done')
   
