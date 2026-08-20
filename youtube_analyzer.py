import re
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    """Extract YouTube video ID from common YouTube URL formats."""
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

    # فقط برای گرفتن عنوان و توضیحات.
    # اگر yt-dlp به خاطر Bot-check شکست خورد،
    # Transcript همچنان می‌تواند با API جداگانه دریافت شود.
    title = None
    description = None

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["web_embedded", "android_vr"]
                }
            },
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get("title")
        description = info.get("description")

    except Exception as e:
        print("YOUTUBE INFO WARNING:", str(e))

    # Transcript را مستقیم با youtube-transcript-api می‌گیریم.
    transcript = get_transcript(video_id)

    return {
        "title": title or "YouTube Video",
        "description": description or "",
        "transcript": transcript,
    }


def get_transcript(video_id):
    api = YouTubeTranscriptApi()

    # ابتدا انگلیسی را امتحان می‌کنیم.
    languages = ["en"]

    try:
        transcript = api.fetch(
            video_id,
            languages=languages
        )

        parts = []

        for item in transcript:
            text = getattr(item, "text", None)

            if text:
                parts.append(text)

        result = " ".join(parts)

        result = re.sub(r"\s+", " ", result).strip()

        if result:
            print("YOUTUBE TRANSCRIPT SUCCESS:", len(result), "characters")
            return result

    except Exception as e:
        print("ENGLISH TRANSCRIPT WARNING:", str(e))

    # اگر انگلیسی موجود نبود، زبان‌های رایج دیگر را امتحان می‌کنیم.
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
                languages=[language]
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
                    "characters"
                )
                return result

        except Exception as e:
            print(
                "TRANSCRIPT WARNING",
                language,
                ":",
                str(e)
            )

    return None
