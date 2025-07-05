# 🎧 jukerstone-spotify-downloader

A direct Spotify Connect downloader by **Jukerstone™**, powered by Python, Spotipy, librespot, and ffmpeg.

✅ Turns your machine into a Spotify Connect device  
✅ Records the raw stream from Spotify servers (via librespot)  
✅ Captures exactly one track in high quality, saves as MP3  
✅ No sketchy network sniffing — uses official Spotify Connect protocol

---

## 🚀 Features

- Starts a `librespot` device called **PythonDownloader**
- Waits until you play a song on it from your Spotify app
- Checks that the track is at the start, seeks if needed
- Records exactly the track duration plus buffer
- Outputs a clean MP3 file named `Artist - Title.mp3`

---

## 📦 Requirements

### Python packages

Install with pip:

```bash
pip install -r requirements.txt
```

This installs:

- `spotipy`  → Handles Spotify Web API auth & control
