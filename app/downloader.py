import os
import asyncio
import time

from yt_dlp import YoutubeDL
from aiogram.types import Message




def yt_download_sync(url: Message, progress_queue: asyncio.Queue, loop, path: str, res, med) -> list:
    v_res = 0
    for i in range(len(res)):
        if "✅" in res[i]:
            v_res = i

    v_med = 0
    for i in range(len(med)):
        if "✅" in med[i]:
            v_med = i

    base_opts = {"quiet": True, "skip_download": True}
    info = YoutubeDL(base_opts).extract_info(url.text, download=False)
    results = []

    if info.get("_type") == "playlist":
        for entry in info["entries"]:
            if entry is None:
                continue
            entry_url = entry.get("webpage_url")
            path = _download_single(entry_url, progress_queue, loop, path, v_res, v_med)
            results.append(path)

    else:

        path = _download_single(url.text, progress_queue, loop, path, v_res, v_med)
        results.append(path)

    return results



def _download_single(url: str, progress_queue: asyncio.Queue, loop, path, v_res, v_med) -> str:

    def my_hook(d):
        if d['status'] == 'downloading':
            asyncio.run_coroutine_threadsafe(progress_queue.put(d.get("_percent_str")), loop)
        if d['status'] == 'finished':
            asyncio.run_coroutine_threadsafe(progress_queue.put("DONE"), loop)

    info = YoutubeDL({"quiet": True, "skip_download": True}).extract_info(url, download=False)
    avail_res = ["4320","2160","1440","1080","720","480","360","240","140"]
    is_video = not "music" in url
    if (is_video and v_med == 0) or v_med == 1 :
        ydl_opts = {
        "max_filesize": 2*1024*1024*1024,
        "format": f"bv*[vcodec!*=av01][height<={avail_res[v_res]}][filesize<2G]+ba[filesize<2G]",
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [my_hook],
        "quiet": True,
        "retries": 10,
        "merge_output_format": "mp4",
        "cookiefile":"cookies.txt",
    }
    elif (not is_video and v_med == 0) or v_med == 2:
        ydl_opts = {
            "max_filesize": 2*1024*1024*1024,
            "format": "bestaudio[filesize<2G]/best[filesize<2G]",
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
            "progress_hooks": [my_hook],
            "quiet": True,
            "retries": 10,
            "prefer_ffmpeg": True,
            "merge_output_format": "mp3",
            "cookiefile": "cookies.txt",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        }
    elif v_med == 3:
        ydl_opts = {
            "max_filesize": 2*1024*1024*1024,
            "format": f"bv*[vcodec!*=av01][height<={avail_res[v_res]}][filesize<2G]",
            "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
            "progress_hooks": [my_hook],
            "quiet": True,
            "retries": 10,
            "prefer_ffmpeg": True,
            "merge_output_format": "mp4",
            "cookiefile": "cookies.txt",
            "postprocessors": [{
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4",
            },
            {
                'key': 'FFmpegAudioRemover'
            }
          ]
        }
    else:
        return ""
    with YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=True)
        filepath = ydl.prepare_filename(result)

    if (not is_video and v_med == 0) or v_med == 2:
        return filepath.rsplit(".", 1)[0] + ".mp3"
    return filepath
