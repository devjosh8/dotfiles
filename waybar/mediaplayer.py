import subprocess
import json
import time

def spotify_status():
    result = subprocess.run(["playerctl", "--player=spotify", "status"], capture_output=True, text=True)
    result = result.stdout.strip()
    if result == "Paused":
        return "Paused"
    elif result == "No players found":
        return "Not Found"
    elif result == "Playing":
        return "Playing"
    else:
        return "Unknown"

def parse_spotify_data(data):
    parsed_data = {}
    artist, title = None, None  # Initialize artist and title
    
    lines = data.splitlines()
    for line in lines:
        if "artist" in line:
            index = line.find("artist") + len("artist")
            artist = line[index:].strip()
        elif "title" in line:
            index = line.find("title") + len("title")
            title = line[index:].strip()

    if artist and title:
        return f"{artist} - {title}"
    else:
        return "Unknown song"

def main():
    last_song = ""
    scroll_index = 0

    show_amount = 40
    scroll_step = 5
    scroll_speed = 1.0  # Sekunden pro Scrollschritt
    status_check_interval = 5.0  # Sekunden

    last_status_check = 0
    status = "Unknown"

    while True:
        now = time.time()
        if now - last_status_check > status_check_interval:
            status = spotify_status()
            last_status_check = now

            if status == "Paused":
                to_write = "Spotify Is Paused"
            elif status == "Playing":
                result = subprocess.run(["playerctl", "--player=spotify", "metadata"], capture_output=True, text=True)
                to_write = parse_spotify_data(result.stdout) + " "
            else:
                to_write = "Spotify Is Offline"

            if to_write != last_song:
                scroll_index = 0
                last_song = to_write

        if len(last_song) <= show_amount:
            result_string = last_song
        else:
            double_text = last_song + last_song[:show_amount]
            scroll_index = scroll_index % len(last_song)
            result_string = double_text[scroll_index:scroll_index + show_amount]
            scroll_index += scroll_step

        # Icon setzen je nach Status
        if status == "Playing":
            icon = ""  # Play-Icon (kannst du anpassen)
        else:
            icon = ""  # X-Icon (kein Sound)

        data = {'text': result_string, 'icon': icon}
        print(json.dumps(data, ensure_ascii=False))

        time.sleep(scroll_speed)

if __name__ == "__main__":
    main()
