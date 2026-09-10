import re
from yt_dlp import YoutubeDL
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    patterns = [
        r"(?:youtube\.com/watch\?v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_transcript(video_id):
    api = YouTubeTranscriptApi()

    # New youtube-transcript-api API
    if hasattr(api, "fetch"):
        try:
            transcript = api.fetch(
                video_id,
                languages=["fa", "en"]
            )

            return " ".join(
                item.text for item in transcript
            )
        except Exception:
            pass

    # Compatibility with older versions
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["fa", "en"]
        )

        return " ".join(
            item["text"] for item in transcript
        )
    except Exception:
        return None


def get_video_info(url):
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    # Get video metadata
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    title = info.get("title") or "Untitled"

    transcript = get_transcript(video_id)

    return {
        "title": title,
        "transcript": transcript,
        "video_id": video_id,
        "url": url,
    }
