import requests
import logging
from lyricsgenius import Genius
import os

# Set up the Genius API credentials
access_token = ""
base_url = "https://api.genius.com"
genius = Genius(access_token)

# Define the artist ID
artist_id = 4

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to retrieve all songs by the artist
def get_artist_songs(artist_id):
    endpoint = f"/artists/{artist_id}/songs"
    url = base_url + endpoint
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "per_page": 50,  # Number of songs per page
        "page": 1,  # Initial page number
    }
    songs = []

    while True:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()["response"]

        songs.extend(data["songs"])
        logging.info(f"found: {len(songs)}")


        if data["next_page"] :
            params["page"] += 1
        else:
            break

    return songs

# Function to retrieve the lyrics for a song
def get_song_lyrics(song_id):
    try:
        lyrics = genius.lyrics(song_id=song_id , remove_section_headers=True) 
        return lyrics
    except:
        return ""

# Main script
if __name__ == "__main__":
    # Retrieve all songs by the artist
    songs = get_artist_songs(artist_id)
    total_songs = len(songs)
    logging.info(f"Total songs: {total_songs}")
    saved_songs = 0
            
    for song in songs:
        song_id = song["id"]
        filename = "wayne/" + str(song_id)
        if os.path.exists(filename):
            logging.info(f"Skipping song ID {song_id} as the file already exists.")
            continue
        with open(filename, "w", encoding="utf-8") as file:
            lyrics = get_song_lyrics(song_id)
            if lyrics:
                file.write(lyrics.strip() + "\n\n")
                saved_songs += 1
                logging.info(f"Saved lyrics for song ID: {song_id}")


    logging.info(f"Saved songs: {saved_songs}")
    print("Lyrics saved to all_lyrics.txt")

    # Log the number of fetched songs
    logging.info(f"Fetched songs: {total_songs}")
