import os
import re
import time
import requests

SUPADATA_API_URL = "https://api.supadata.ai/v1/transcript"
SUPADATA_JOB_URL = "https://api.supadata.ai/v1/transcript"


def extract_video_id(url):
    patterns = [
        r"(?:v=)([A-Za-z0-9_-]{11})",
        r"(?:youtu\.be/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/shorts/)([A-Za-z0-9_-]{11})",
        r"(?:youtube\.com/embed/)([A-Za-z0-9_-]{11})",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", str(text))
    return text.strip()


def extract_transcript(data):
    content = data.get("content") if isinstance(data, dict) else None

    if isinstance(content, list):
        parts = []

        for item in content:
            if isinstance(item, dict):
                text = item.get("text")
                if text:
                    parts.append(str(text))
            elif isinstance(item, str):
                parts.append(item)

        return clean_text(" ".join(parts))

    if isinstance(content, str):
        return clean_text(content)

    return ""


def get_video_info(url):
    video_id = extract_video_id(url)

    print("YOUTUBE ANALYZER: VIDEO ID =", video_id, flush=True)

    if not video_id:
        raise ValueError("Invalid YouTube URL")

    api_key = os.environ.get("SUPADATA_API_KEY")

    if not api_key:
        raise RuntimeError("SUPADATA_API_KEY is not configured")

    headers = {
        "x-api-key": api_key
    }

    params = {
        "url": url,
        "lang": "en"
    }

    response = requests.get(
        SUPADATA_API_URL,
        params=params,
        headers=headers,
        timeout=45
    )

    print("SUPADATA STATUS:", response.status_code, flush=True)

    if response.status_code == 200:
        try:
            data = response.json()
        except Exception:
            print("SUPADATA JSON ERROR:", response.text[:500], flush=True)
            raise RuntimeError("Invalid response from Supadata")

        transcript = extract_transcript(data)

        if transcript:
            print(
                "SUPADATA TRANSCRIPT SUCCESS:",
                len(transcript),
                "chars",
                flush=True
            )

        return {
            "title": "YouTube Video",
            "transcript": transcript or None,
            "video_id": video_id,
            "url": url
        }

    if response.status_code != 202:
        print(
            "SUPADATA REQUEST ERROR:",
            response.text[:1000],
            flush=True
        )
        raise RuntimeError(
            f"Supadata returned HTTP {response.status_code}: "
            f"{response.text[:500]}"
        )

    try:
        job_data = response.json()
    except Exception:
        raise RuntimeError("Supadata returned invalid job response")

    job_id = job_data.get("jobId")

    if not job_id:
        raise RuntimeError("Supadata returned 202 but no jobId")

    print("SUPADATA JOB ID:", job_id, flush=True)

    # Poll the job until the transcript is ready.
    for attempt in range(12):
        time.sleep(2)

        job_response = requests.get(
            f"{SUPADATA_JOB_URL}/{job_id}",
            headers=headers,
            timeout=45
        )

        print(
            "SUPADATA JOB STATUS:",
            job_response.status_code,
            "ATTEMPT:",
            attempt + 1,
            flush=True
        )

        if job_response.status_code != 200:
            continue

        try:
            job_result = job_response.json()
        except Exception:
            continue

        transcript = extract_transcript(job_result)

        if transcript:
            print(
                "SUPADATA TRANSCRIPT SUCCESS:",
                len(transcript),
                "chars",
                flush=True
            )

            return {
                "title": "YouTube Video",
                "transcript": transcript,
                "video_id": video_id,
                "url": url
            }

        status = str(
            job_result.get("status", "")
        ).lower()

        print(
            "SUPADATA JOB RESULT STATUS:",
            status,
            flush=True
        )

        if status in ("failed", "error", "cancelled"):
            break

    print("SUPADATA: NO TRANSCRIPT", flush=True)

    return {
        "title": "YouTube Video",
        "transcript": None,
        "video_id": video_id,
        "url": url
    }
