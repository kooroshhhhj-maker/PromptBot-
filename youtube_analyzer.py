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
    print("========== YOUTUBE TRANSCRIPT DEBUG ==========")
    print("VIDEO ID:", video_id)

    try:
        api = YouTubeTranscriptApi()

        print("TRANSCRIPT API: fetching English transcript...")

        transcript = api.fetch(
            video_id,
            languages=["en"],
        )

        print("TRANSCRIPT API: fetch SUCCESS")
        print("TRANSCRIPT OBJECT TYPE:", type(transcript).__name__)
        print(
            "LANGUAGE:",
            getattr(transcript, "language_code", None)
        )
        print(
            "GENERATED:",
            getattr(transcript, "is_generated", None)
        )

        parts = []

        for item in transcript:
            text = getattr(item, "text", None)

            if text:
                parts.append(text)

        result = " ".join(parts)
        result = re.sub(r"\\s+", " ", result).strip()

        print(
            "YOUTUBE TRANSCRIPT SUCCESS:",
            len(result),
            "characters"
        )

        if result:
            print("==============================================")
            return result

        print("TRANSCRIPT RESULT IS EMPTY")
        print("==============================================")

    except Exception as e:
        import traceback

        print("!!!!!!!! YOUTUBE TRANSCRIPT ERROR !!!!!!!!")
        print("ERROR TYPE:", type(e).__name__)
        print("ERROR:", repr(e))
        traceback.print_exc()
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

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
            print(
                "TRANSCRIPT FALLBACK:",
                language
            )

            api = YouTubeTranscriptApi()

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
            result = re.sub(r"\\s+", " ", result).strip()

            if result:
                print(
                    "YOUTUBE TRANSCRIPT SUCCESS:",
                    language,
                    len(result),
                    "characters"
                )
                print("==============================================")
                return result

        except Exception as e:
            import traceback

            print(
                "FALLBACK ERROR:",
                language,
                type(e).__name__,
                repr(e)
            )
            traceback.print_exc()

    print("YOUTUBE TRANSCRIPT FAILED COMPLETELY")
    print("==============================================")

    return None
