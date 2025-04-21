# Setlist-to-Spotify-Python

A project that aims to turn a listed setlist from setlist.fm into a Spotify playlist for the user. using both API's from Spotify and setlist.fm.

The first step would be to build the backend of the Spotify API part. This would be broken into the following parts:

    1. I have set up a function that locates the ID of Spotify user, as well as a function that generates a user token, which allows permissions for changes to be made on the users profile (Creating a playlist for example).

    2. A function dedicated to creating playlists is created. This returns a playlist ID, which will be used when adding the tracks.

    3. Passing a list of songs, as well as a band name into the search_item function. the data would be parsed, and each Spotify ID for each track would be pushed into an empty list. This would then return a list of Spotify id's for each track.

    4. The list of spotify ID's is then passed into the search_tracks function. which then be parsed and a Spotify url is then returned and pushed into another empty list. This would then return a list of Spotify url's.

    5. This new list of Spotify url's will then be passed into the add_to_playlist function. Which will take the list of urls and in turn, add them to the playlist, using the aforementioned playlist ID.

The next step will be to use the setlist.fm API to pull the required information through. Such as the artist name and the list of songs which will be then passed into the Spotify API.
