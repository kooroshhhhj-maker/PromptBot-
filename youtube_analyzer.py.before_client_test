import re
import requests
import yt_dlp


def get_video_info(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    return {
        "title": info.get("title"),
        "description": info.get("description"),
        "transcript": get_transcript(info),
    }


def get_transcript(info):
    captions = info.get("automatic_captions") or {}

    # اولویت با زیرنویس انگلیسی
    if "en" not in captions:
        return None

    caption_url = captions["en"][0]["url"]

    response = requests.get(
        caption_url,
        timeout=30,
    )
    response.raise_for_status()

    data = response.json()

    parts = []

    for event in data.get("events", []):
        for seg in event.get("segs", []):
            text = seg.get("utf8")

            if text:
                parts.append(text)

    transcript = " ".join(parts)

    # تمیز کردن فاصله‌ها
    transcript = re.sub(r"\s+", " ", transcript).strip()

    return transcript
