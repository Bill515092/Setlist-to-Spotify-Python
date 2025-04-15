from dotenv import load_dotenv
import os
import base64
import requests
from requests import post, get
import json
import webbrowser

load_dotenv()


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_URI = os.getenv("REDIRECT_URI")
scopes = "user-read-private user-read-email playlist-modify-public playlist-modify-private"
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={redirect_URI}&scope={scopes}"
webbrowser.open(auth_url)

auth_code = input("Paste the authorization code from URL: ")

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
def search_item(token):
    url = "https://api.spotify.com/v1/search" 
    headers = get_auth_header(token)
    params = {
        "q": "remaster track:Doxy artist:Miles Davis",
        "type": "track"
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching user info:", response.json()) 
        return None
    
    data = response.json()
    items = data.get("tracks").get("items")

    return items[0]["id"]

# Create a function to search for a list of songs add them to an array (Spotify URI's). Pass the found spotift ID's
def search_tracks(token, spotify_id):
    url = "https://api.spotify.com/v1/tracks"
    headers = get_auth_header(token)
    params = {
        "market": "UK",
        "ids": spotify_id  
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print("Error fetching user info:", response.json()) 
        return None
    
    data = response.json()

    return data.get("tracks")[0]["uri"]
    
# Create a function to add items to a playlist, and pass the song array variable in the bost of the request.
def add_to_playlist(token, spotify_uri, playlist_id):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = get_auth_header(token)
    body = {
        "uris": [spotify_uri],
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


spotify_id = search_item(token)
# print(spotify_id)

spotify_uris = search_tracks(token, spotify_id)
# print(spotify_uris)

playlist_id = create_playlist(token, user_id)
# print(playlist_id)

create_playlist(token, user_id)
add_to_playlist(token, spotify_uris, playlist_id)
