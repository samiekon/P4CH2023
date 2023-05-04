from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import csv
from bs4 import BeautifulSoup

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type" : "application/x-www-form-urlencoded"
    }
    data = {"grant_type" : "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"

    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    
    return json_result[0]

def get_songs_by_artists(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

html = open('Women-In-Electronic-Music.html').read()
soup = BeautifulSoup(html, 'html.parser')

all_artists = {}

for tr in soup.find_all('tr'):

    if len(tr.find_all('th')) > 0:
        continue

    artist = tr.find_all('td')[0].text
    wikidata_url = tr.find('a')['href']
    song = tr.find_all('td')[1].text      
    year = tr.find_all('td')[2].text       
    print(artist,wikidata_url,song,year)

    if artist not in all_artists:
        all_artists[artist] = {
            'songs': [],
            'name': artist,
            'spotify_follower_count': None,
            'genres': [],
            'spotify': None, 
            'spotify_name': None,
            'spotify_id': None,
            'wikidata_url': wikidata_url,
            'image': None,
            'Qnuber': wikidata_url.split('/')[-1] 
        }

    song = {
        'name': song,
        'year': year,
        'spotify': None, 
        'spotify_preview': None
    }

    all_artists[artist]['songs'].append(song)

token = get_token()

for artist in all_artists:
    print('doing ',artist)
    result = search_for_artist(token, artist)

    all_artists[artist]['spotify'] = result['external_urls']['spotify']
    all_artists[artist]['spotify_follower_count'] = result['followers']['total']
    all_artists[artist]['genres'] = result['genres']

    if 'images' in result:
        if len(result['images']) > 0:

            all_artists[artist]['image'] = result['images'][0]['url']

    all_artists[artist]['spotify_name'] = result['name']

   
    all_artists[artist]['spotify_id'] = result['id']

    
    artist_id = result["id"]

    songs = get_songs_by_artists(token, artist_id)
    for idx, song in enumerate(songs):
        print(song)
        
        song = {
            'name' : song['name'],
            'spotify': song['external_urls']['spotify'],
            'spotify_preview': song['preview_url']
        }

        all_artists[artist]['songs'].append(song)

        json.dump(all_artists,open('artists.json','w'),indent=2)









