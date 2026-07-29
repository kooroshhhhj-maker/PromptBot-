from PIL import Image
from io import BytesIO

from vision_client import analyze_image


def extract_gif_frames(file_bytes, max_frames=5):
    try:
        image = Image.open(BytesIO(file_bytes))

        frames = []

        total = getattr(image, "n_frames", 1)

        for i in range(min(max_frames, total)):
            image.seek(i)

            frame = image.convert("RGB")

            buffer = BytesIO()
            frame.save(
                buffer,
                format="JPEG",
                quality=85
            )

            frames.append(buffer.getvalue())

        print("GIF FRAMES:", len(frames))

        return frames

    except Exception as e:
        print("GIF ERROR:", e)
        return []


def analyze_gif(file_bytes):

    print("GIF ANALYSIS START")

    frames = extract_gif_frames(file_bytes)

    if not frames:
        return "❌ نتوانستم فریم‌های GIF را استخراج کنم."

    results = []

    for index, frame in enumerate(frames):

        print("ANALYZING FRAME:", index + 1)

        result = analyze_image(frame)

        if result:
            results.append(
                f"فریم {index+1}:\n{result}"
            )

    if results:
        return "\n\n".join(results)

    return "❌ تحلیل GIF نتیجه‌ای نداشت."

