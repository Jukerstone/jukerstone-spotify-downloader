import subprocess
import time
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# === CONFIG ===
SPOTIPY_CLIENT_ID = 'enter-client-id'
SPOTIPY_CLIENT_SECRET = 'enter-client-secret'
SPOTIPY_REDIRECT_URI = 'http://localhost:8888/callback'
SCOPE = 'user-read-playback-state,user-modify-playback-state'

# === INIT SPOTIPY ===
sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# === START LIBRESPOT ===
print("🚀 Starting librespot...")
librespot_process = subprocess.Popen([
    "librespot",
    "--name", "PythonDownloader",
    "--backend", "pipe",
    "--disable-audio-cache",
    "--bitrate", "160"
], stdout=subprocess.PIPE)

time.sleep(5)
print("✅ librespot started. Please open Spotify, select 'PythonDownloader' and start your song.")

# === WAIT FOR PLAYBACK ON PYTHONDOWNLOADER ===
while True:
    playback = sp.current_playback()
    if playback and playback.get('is_playing'):
        device_name = playback['device']['name']
        if device_name == "PythonDownloader":
            break
        else:
            print(f"🎧 Currently playing on '{device_name}', waiting for 'PythonDownloader'...")
    else:
        print("⏳ Waiting for playback to start on 'PythonDownloader'...")
    time.sleep(2)

track = playback['item']
track_name = track['name']
artist_name = track['artists'][0]['name']
duration_ms = track['duration_ms']
duration_sec = int(duration_ms / 1000)

print(f"🎧 Detected on 'PythonDownloader': {artist_name} - {track_name}")
print(f"📏 Duration: {duration_sec}s")

# === IF NOT AT START, SEEK TO 0 ===
progress_ms = playback['progress_ms']
if progress_ms > 0:
    print(f"↩️ Not at start (at {int(progress_ms/1000)}s). Seeking to 0...")
    sp.seek_track(0)
    time.sleep(1)

# === WAIT UNTIL CONFIRMED AT START ===
while True:
    playback = sp.current_playback()
    if (playback and playback['is_playing']
        and playback['device']['name'] == "PythonDownloader"):
        if playback['progress_ms'] <= 2000:
            break
    time.sleep(0.5)

output_filename = f"{artist_name} - {track_name}.mp3".replace("/", "_")
print(f"🎯 Recording from exact start on 'PythonDownloader' for {duration_sec} seconds...")

# === START FFMPEG ===
ffmpeg_process = subprocess.Popen([
    "ffmpeg",
    "-f", "s16le",
    "-ar", "44100",
    "-ac", "2",
    "-i", "-",
    "-t", str(duration_sec),
    "-codec:a", "libmp3lame",
    "-qscale:a", "2",
    output_filename
], stdin=librespot_process.stdout)

try:
    ffmpeg_process.communicate()
except KeyboardInterrupt:
    print("⛔ Interrupted by user. Stopping...")
finally:
    librespot_process.terminate()
    ffmpeg_process.terminate()

print(f"✅ Finished recording. Saved to: {output_filename}")
