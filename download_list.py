import yt_dlp
from pathlib import Path
import shutil

if not shutil.which("ffmpeg"):
    raise RuntimeError("FFmpeg not found in PATH. Install before proceeding.")
if not shutil.which("node"):
    print("WARNING: Node.js not found. Download may fail with error 403.")


def download(query, formato="mp3"):
    output_dir = Path("output") / formato
    output_dir.mkdir(parents=True, exist_ok=True)

    if formato == ("mp3" or "3"):
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "extractor_args": {
                "youtube": {
                    "player_client": ["android"]
                }
            },
            "quiet": False,
        }

    elif formato == ("mp4" or "4"):
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",
            "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
            "quiet": False,
        }
    else:
        raise ValueError("Invalid format. Choose 'mp3' or 'mp4'.")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])


def progress_hook(d):
    if d["status"] == "downloading":
        downloaded = d.get("downloaded_bytes", 0)
        total = d.get("total_bytes") or d.get("total_bytes_estimate")

        if total:
            percent = downloaded / total * 100
            speed = d.get("speed", 0)
            eta = d.get("eta", 0)

            print(
                f"\r⬇ {percent:5.1f}% | "
                f"{downloaded / 1e6:6.1f}MB / {total / 1e6:6.1f}MB | "
                f"{speed / 1e6:4.1f}MB/s | ETA {eta:3}s",
                end="",
                flush=True,
            )

    elif d["status"] == "finished":
        print("\nDownload finished. Processing file...")


def main():
    formato = input("Pick a format (mp3/mp4): ").strip().lower()

    with open("list.txt", "r", encoding="utf-8") as f:
        for linha in f:
            query = linha.strip()
            if query:
                print(f"Downloading: {query}")
                download(query, formato)


if __name__ == "__main__":
    main()
