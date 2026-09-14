import requests
import json
import time
from io import BytesIO

BASE_URL = "https://mastap-wan22-remix-sfw-t2v.hf.space"


def generate_video(prompt, seconds=3.0, steps=8, guidance_scale=1.0):
    try:
        print("VIDEO: Starting generation...")

        payload = {
            "data": [
                prompt,
                "",
                seconds,
                steps,
                guidance_scale,
                0,
                True
            ]
        }

        r = requests.post(
            BASE_URL + "/gradio_api/call/generate_video",
            json=payload,
            timeout=30
        )

        print("VIDEO SUBMIT:", r.status_code, r.text)

        if not r.ok:
            return None

        event_id = r.json()["event_id"]

        print("VIDEO EVENT:", event_id)
        print("VIDEO: Waiting...")

        r = requests.get(
            BASE_URL + "/gradio_api/call/generate_video/" + event_id,
            timeout=600
        )

        if not r.ok:
            print("VIDEO POLL ERROR:", r.status_code)
            return None

        for line in r.text.splitlines():
            if not line.startswith("data:"):
                continue

            data = line[5:].strip()

            if not data or data == "null":
                continue

            try:
                result = json.loads(data)
            except Exception:
                continue

            if isinstance(result, list) and result:
                file_data = result[0]

                if isinstance(file_data, dict) and file_data.get("url"):
                    video_url = file_data["url"]

                    print("VIDEO URL:", video_url)

                    video = requests.get(
                        video_url,
                        timeout=120
                    )

                    if not video.ok:
                        print("VIDEO DOWNLOAD ERROR:", video.status_code)
                        return None

                    output = BytesIO(video.content)
                    output.name = "promptbot_video.mp4"
                    output.seek(0)

                    print(
                        "VIDEO READY:",
                        len(video.content),
                        "bytes"
                    )

                    return output

        print("VIDEO: No video returned")
        return None

    except Exception as e:
        print("VIDEO ERROR:", repr(e))
        return None
