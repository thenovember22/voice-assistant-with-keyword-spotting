music = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "perfect": "https://youtube.com/clip/UgkxxNzKUW_02tTlXwIycroIwUeJbOJBdfKb?si=4QfNd24w_zusw0xr",
    "senorita": "https://www.youtube.com/watch?v=Pkh8UtuejGw",
    "wonder": "https://youtube.com/clip/Ugkx8_SdQrkvIphXUGvrxcitcEWRffybbWf0?si=79DlPogjW8bbM90W",
}


def get_song_link(song_name: str):
    return music.get(song_name.strip().lower())
