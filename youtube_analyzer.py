import re

import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    patterns = [
        r"(?:youtube\.com/watch\?v=)([^&]+)",
        r"(?:youtu\.be/)([^?&]+)",
        r"(?:youtube\.com/shorts/)([^?&]+)",
        r"(?:youtube\.com/embed/)([^?&]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_video_info(url):
    video_id = extract_video_id(url)

    if not video_id:
        raise ValueError("لینک YouTube معتبر نیست.")

    title = "YouTube Video"
    description = ""

    # فقط برای اطلاعات جانبی؛ شکست آن نباید Transcript را خراب کند.
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "socket_timeout": 10,
            "extractor_args": {
                "youtube": {
                    "player_client": [
                        "web_embedded",
                        "android_vr",
                    ]
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(
                f"https://www.youtube.com/watch?v={video_id}",
                download=False,
            )

        title = info.get("title") or title
        description = info.get("description") or ""

    except Exception as e:
        print("YOUTUBE INFO WARNING:", str(e))

    # Transcript مستقل از yt-dlp
    transcript = get_transcript(video_id)

    return {
        "title": title,
        "description": description,
        "transcript": transcript,
    }


def get_transcript(video_id):
    api = YouTubeTranscriptApi()

    # اول انگلیسی
    languages = ["en"]

    try:
        transcript = api.fetch(
            video_id,
            languages=languages,
        )

        parts = []

        for item in transcript:
            text = getattr(item, "text", None)

            if text:
                parts.append(text)

        result = " ".join(parts)
        result = re.sub(r"\s+", " ", result).strip()

        if result:
            print(
                "YOUTUBE TRANSCRIPT SUCCESS:",
                len(result),
                "characters",
            )
            return result

    except Exception as e:
        print(
            "ENGLISH TRANSCRIPT WARNING:",
            str(e),
        )

    # زبان‌های جایگزین
    fallback_languages = [
        "fa",
        "ar",
        "tr",
        "de",
        "fr",
        "es",
    ]

    for language in fallback_languages:
        try:
            transcript = api.fetch(
                video_id,
                languages=[language],
            )

            parts = []

            for item in transcript:
                text = getattr(item, "text", None)

                if text:
                    parts.append(text)

            result = " ".join(parts)
            result = re.sub(r"\s+", " ", result).strip()

            if result:
                print(
                    "YOUTUBE TRANSCRIPT SUCCESS:",
                    language,
                    len(result),
                    "characters",
                )
                return result

        except Exception as e:
            print(
                "TRANSCRIPT WARNING",
                language,
                ":",
                str(e),
            )

    return None
