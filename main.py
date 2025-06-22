from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json
import webbrowser

load_dotenv()

my_email = os.getenv("EMAIL_ADDRESS")
setlist_key = os.getenv("SETLIST_KEY")
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_URI = os.getenv("REDIRECT_URI")
scopes = "user-read-private user-read-email playlist-modify-public playlist-modify-private"
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_URI}&scope={scopes}"
webbrowser.open(auth_url)

auth_code = input("Paste the authorization code from URL: ")

# band_name can be filled with the user input.
mb_band_name = "Sleep Token"

# band_name = "Sleep Token" 
setlist = ["Euclid", "The Summoning", "Caramel", "Damocles", "Alkaline"]
id_arr = []
uri_arr = []

def get_mbid(mb_band_name, email):
    url = f"https://musicbrainz.org/ws/2/artist/?query=artist:{mb_band_name}&fmt=json"
    headers = {"User-Agent": f"setlist_to_spotify ({email})"}
    response = requests.get(url, headers=headers)
    data = response.json().get("artists")[0]["id"]

    if response.status_code != 200:
        print("Error fetching user info:", data) 

    return data

def get_token(auth_code):
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_URI
            }
    
    response = requests.post(url, headers=headers, data=data)
    token_info = response.json()

    if "access_token" not in token_info:
        print("Error getting token:", token_info) 
        return None  

    return token_info["access_token"] 

def get_auth_header(token):
    return {"Authorization": f"Bearer {token}"}

def get_user_id(token):
    url = "https://api.spotify.com/v1/me"
    headers = get_auth_header(token)
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print("Error fetching user info:", response.json()) 
        return None
    
    return response.json().get("id")

def create_playlist(token, user_id):

    url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = get_auth_header(token)
    body = {
        "name": "Test Playlist",
        "description": "Test playlist description",
        "public": False
    }
    data = json.dumps(body)
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 201:
        print("Error fetching user info (Create Playlist):", response.json()) 
        return None

    return response.json()["id"]
# Create a function that searches for an item. Can get the spotify ID of the track(s)
def search_item(token, band_name, setlist):

    for i in setlist:
        
        url = "https://api.spotify.com/v1/search" 
        headers = get_auth_header(token)
        params = {
            "q": f"track:{i} artist:{band_name}",
            "type": "track",
            "market": "GB"
        }
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print("Error fetching user info:", response.json()) 
            return None
        
        data = response.json()
        items = data.get("tracks").get("items")
        artist_details = data.get("tracks").get("items")[0]["artists"]

        if items[0]["name"] == i and artist_details[0]["name"] == band_name:
            id_arr.append(items[0]["id"])
        else:
            "We are unable to find this song. Please select another."

    return id_arr    
# Create a function to search for a list of songs add them to an array (Spotify URI's). Pass the found spotift ID's
def search_tracks(token, spotify_ids):
    
    spotify_ids = ",".join(spotify_ids)
    url = "https://api.spotify.com/v1/tracks"
    headers = get_auth_header(token)
    params = {
        "market": "UK",
        "ids": spotify_ids
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching user info:", response.json()) 
        return None
    
    data = response.json()
    index = 0

    while len(uri_arr) < len(id_arr):
        uri = data.get("tracks")[index]["uri"]
        uri_arr.append(uri)
        index += 1
    
    return uri_arr    
# Create a function to add items to a playlist, and pass the song array variable in the bost of the request.
def add_to_playlist(token, spotify_uris, playlist_id):

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    body = {
        "uris": spotify_uris,
        "position": 0
    }
    data = json.dumps(body)
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code != 201:
        print("Error fetching user info (Create Playlist):", response.json()) 
        return None
    
    return response.json()

    

token = get_token(auth_code)

if token:
    user_id = get_user_id(token)
    # print("User ID:", user_id)
else:
    print("Failed to retrieve token.")

mbid = get_mbid(mb_band_name, my_email)

# search_item(token, band_name, setlist)
# # print(id_arr)
# search_tracks(token, id_arr)
# # print("uri array =", uri_arr)
# playlist_id = create_playlist(token, user_id)
# # print(playlist_id)
# add_to_playlist(token, uri_arr, playlist_id)
