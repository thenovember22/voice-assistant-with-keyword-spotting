music = {
    "shape of you": "https://www.youtube.com/watch?v=JGwWNGJdvx8",
    "perfect": "https://youtube.com/clip/UgkxxNzKUW_02tTlXwIycroIwUeJbOJBdfKb?si=4QfNd24w_zusw0xr",
    "senorita": "https://www.youtube.com/watch?v=Pkh8UtuejGw",
    "wonder": "https://youtube.com/clip/Ugkx8_SdQrkvIphXUGvrxcitcEWRffybbWf0?si=79DlPogjW8bbM90W",
}


def normalize_song_name(song_name: str) -> str:
    import unicodedata

    normalized = unicodedata.normalize("NFKD", song_name.casefold())
    without_accents = "".join(
        char for char in normalized if not unicodedata.combining(char)
    )
    return " ".join(without_accents.strip().split())


def get_song_link(song_name: str):
    return music.get(normalize_song_name(song_name))
