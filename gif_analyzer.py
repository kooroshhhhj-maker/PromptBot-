from PIL import Image
from io import BytesIO


def extract_gif_frames(file_bytes, max_frames=5):
    try:
        image = Image.open(BytesIO(file_bytes))

        frames = []

        for i in range(min(max_frames, getattr(image, "n_frames", 1))):
            image.seek(i)

            frame = image.convert("RGB")

            buffer = BytesIO()
            frame.save(buffer, format="JPEG")

            frames.append(buffer.getvalue())

        return frames

    except Exception as e:
        print("GIF ERROR:", e)
        return []
