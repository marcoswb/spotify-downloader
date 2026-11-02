# Spotify Downloader

Command-line tool that downloads Spotify tracks, albums, and playlists as MP3 files and, for albums and playlists, downloads only the tracks that are not already recorded locally.

Streaming covers day-to-day listening. This project covers the other case: keeping a folder of MP3s in sync with albums and playlists without downloading the whole list again each time.

## Features

- Accepts one or more Spotify track, album, or playlist links in a single run.
- Saves album and playlist links in a local SQLite database (`memory.db`).
- On a later run, compares the current Spotify listing with saved tracks and downloads only the ones that are missing.
- Can refresh every album and playlist already stored in the database.
- Downloads up to 10 tracks at a time and shows a progress bar for each album or playlist.
- Writes files into a folder you choose. Albums and playlists each get a subfolder named after the Spotify title.
- Names album and playlist files from the MP3 title tag. A `/` in the title is replaced with `-`.

## Technologies

- Python 3
- [spotipy](https://spotipy.readthedocs.io/) (`spotipy==2.22.1`) for Spotify Web API metadata
- [spotify-dl](https://pypi.org/project/spotify-dl/) (`spotify-dl==8.3.0`), invoked as the `spotify_dl` command, to produce the MP3 files
- [Peewee](https://docs.peewee-orm.com/) (`peewee~=3.17.8`) and SQLite
- [python-dotenv](https://pypi.org/project/python-dotenv/) (`python-dotenv~=1.0.1`)
- [mutagen](https://mutagen.readthedocs.io/) (`mutagen~=1.45.1`) to read ID3 tags
- [tqdm](https://tqdm.github.io/) for the progress bar


## Project structure

```text
main.py                 Interactive menu and download loop
utils/functions.py      Prompts, Spotify API calls, .env loading, config.ini
utils/Download.py       Skip logic, parallel downloads, file copy
models/Playlist.py      Saved album and playlist links
models/Track.py         Tracks already recorded for those links
models/init_db.py       Creates the SQLite tables on startup
```

Runtime files, created in the working directory and ignored by git:

| File | Purpose |
| --- | --- |
| `.env` | Spotify API credentials |
| `config.ini` | Output folder |
| `memory.db` | Albums, playlists, and tracks already recorded |

## Prerequisites

- Python 3 and `pip`. This repository does not pin a minimum Python version.
- A [Spotify application](https://developer.spotify.com/dashboard/applications) so you can copy its client ID and client secret. The app uses the client-credentials flow and does not sign in as a Spotify user.
- The `spotify_dl` command on your `PATH`. Installing the requirements below provides it.

Run the program from the project directory. `config.ini` and `memory.db` are opened with relative paths.

## Installation

```sh
git clone https://github.com/marcoswb/spotify-downloader.git
cd spotify-downloader
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root:

```text
SPOTIFY_CLIENT_ID=your-client-id
SPOTIFY_CLIENT_SECRET=your-client-secret
```

On startup the program copies those values to `SPOTIPY_CLIENT_ID` and `SPOTIPY_CLIENT_SECRET` for `spotipy` and `spotify_dl`. You do not need to export those names yourself when `.env` is present.

The first run asks for an output folder. The folder must already exist. The answer is stored in `config.ini`:

```ini
[DEFAULT]
output_directory = C:\Music
```

Later runs reuse that path. To change it, edit `output_directory` or delete `config.ini` and answer the prompt again.

## Usage

```sh
python main.py
```

The menu is in Portuguese:

1. **Atualizar todas as playlists** — reload every album and playlist link stored in `memory.db` and download tracks that are not recorded yet.
2. **Baixar novas playlists** — enter one or more links, then press Enter on an empty line to start.

Example links:

```text
https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh
https://open.spotify.com/album/1DFixLWuPkv3KT3TnV35m3
https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M
```

A share link that contains `si=` is trimmed before it is stored.

If an album or playlist is already in the database and you did not choose option 1, the program asks:

```text
Essa playlist já foi baixada uma vez, deseja somente atualizá-la? (S/N)
```

- **S** downloads tracks that are not in the database. If nothing is missing, it prints that the playlist is already up to date.
- **N** deletes the saved track rows for that playlist and downloads its tracks again. Files already in the output folder are not deleted. A new file can overwrite an existing MP3 with the same title.

The same answer is reused for every further album or playlist in that run.

Single tracks are not written to the database. Each request downloads the track again, directly into the output folder rather than a subfolder.

Album and playlist files are saved as:

```text
<output folder>\<album or playlist name>\<title>.mp3
```

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Contact

Marcos Warmling Berti — marcos_wb@outlook.com
