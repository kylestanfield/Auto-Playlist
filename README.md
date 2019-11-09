# Auto Playlist

Auto Playlist will fetch a user's top songs from their Last.fm profile and automatically add them to a Spotify playlist.

## Getting Started

To get your own copy of Auto Playlist, clone this repo into a local directory. Before you can run the Python script, 
you will need to setup a config.ini file with your API keys from Last.fm and Spotify. The config file should have the following form:

```
[API Keys]
last_fm = $YOUR_LAST_FM_API_KEY
spotify = $YOUR_SPOTIFY_API_KEY
```


### Prerequisites

Auto Playlist depends on the Python modules spotipy and requests:

```
pip install spotipy
pip install requests
```


## Built With

* [spotipy](https://github.com/plamere/spotipy) - Spotify API wrapper for Python
* [requests](https://pypi.org/project/requests/2.7.0/) - Simplified HTML requests

## Authors

* **Kyle Stanfield** - *All development*

## License

This project is licensed under the GNU Public License v3.0

## Acknowledgments

Thanks to Paul Lemere for his spotipy library

