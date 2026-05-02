import subprocess
import re


def is_valid_youtube_url(url: str) -> bool:
    pattern = r'^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9_-]{11}'
    return bool(re.match(pattern, url))


def download_video(url: str, output_folder: str) -> dict:
    if not is_valid_youtube_url(url):
        return {"success": False, "error": "Invalid YouTube URL"}

    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-o", f"{output_folder}/%(title)s.%(ext)s",
                "--no-playlist",
                "--extractor-args", "youtube:player_client=mediaconnect",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=600,
        )

        if result.returncode == 0:
            return {"success": True, "output": result.stdout}
        else:
            return {"success": False, "error": result.stderr or "Download failed"}

    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Download timed out (10 min limit)"}
    except FileNotFoundError:
        return {"success": False, "error": "yt-dlp not found. Install it with: pip install yt-dlp"}
