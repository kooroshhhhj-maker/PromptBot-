from PIL import Image
from io import BytesIO
import subprocess
import tempfile
import os

from vision_client import analyze_image
from config import CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID


def extract_gif_frames(file_bytes, max_frames=5):
    try:
        temp_input = tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=False
        )

        temp_input.write(file_bytes)
        temp_input.close()

        output_frames = []

        temp_pattern = tempfile.NamedTemporaryFile(
            suffix=".jpg",
            delete=False
        ).name

        command = [
            "ffmpeg",
            "-i",
            temp_input.name,
            "-vf",
            f"fps=1",
            "-frames:v",
            str(max_frames),
            temp_pattern
        ]

        subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        for i in range(max_frames):
            path = temp_pattern.replace(".jpg", f"{i+1}.jpg")

            if os.path.exists(path):
                with open(path, "rb") as f:
                    output_frames.append(f.read())

        os.unlink(temp_input.name)

        print("GIF FRAMES:", len(output_frames))

        return output_frames

    except Exception as e:
        print("GIF ERROR:", e)
        return []


def analyze_gif(file_bytes):

    frames = extract_gif_frames(file_bytes)

    if not frames:
        return "❌ نتوانستم فریم‌های GIF را استخراج کنم."

    results = []

    for i, frame in enumerate(frames):

        print("ANALYZING FRAME:", i+1)

        result = analyze_image(
            frame,
            CLOUDFLARE_API_TOKEN,
            CLOUDFLARE_ACCOUNT_ID,
            "general"
        )

        if result:
            results.append(
                f"فریم {i+1}:\n{result}"
            )

    if results:
        return "\n\n".join(results)

    return "❌ تحلیل GIF نتیجه‌ای نداشت."

