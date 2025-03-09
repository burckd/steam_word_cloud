import requests
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np


# Replace with your Steam API key and Steam64 ID
STEAM_API_KEY = "INSERT HERE"
STEAM_ID = "INSERT HERE"

# Fetch playtime data from Steam API
def fetch_steam_playtime():
    url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_API_KEY}&steamid={STEAM_ID}&include_appinfo=true&format=json"
    response = requests.get(url)
    data = response.json()

    games = data["response"].get("games", [])
    game_playtime = {game["name"]: game["playtime_forever"] for game in games if "name" in game}

    # Filter out games with less than 60 minutes of playtime
    game_playtime = {name: time for name, time in game_playtime.items() if time >= 10}

    return game_playtime

# Normalize playtime for better word cloud scaling
def normalize_playtime(game_playtime):
    if not game_playtime:
        return {}

    # Convert playtime to log scale to reduce size difference
    min_time = min(game_playtime.values())
    max_time = max(game_playtime.values())

    normalized_playtime = {
        name: (np.log2(time + 1) - np.log2(min_time + 1)) / (np.log2(max_time + 1) - np.log2(min_time + 1)) * 50 + 30
        for name, time in game_playtime.items()
    }
    return normalized_playtime

# Generate word cloud from playtime data
def generate_wordcloud(game_playtime):
    normalized_playtime = normalize_playtime(game_playtime)

    wordcloud = WordCloud(
        width=1920,
        height=1080,
        background_color="white",
        colormap="magma",  # Change this if you want a different color scheme
        max_words=170
    ).generate_from_frequencies(normalized_playtime)

    plt.figure(figsize=(30, 18))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

# Run process
game_playtime = fetch_steam_playtime()
generate_wordcloud(game_playtime)
