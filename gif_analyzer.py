import io
import cv2
from PIL import Image


def extract_gif_frames(video_bytes, frame_count=5):
    video_path = "/tmp/gif.mp4"

    with open(video_path, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(video_path)

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if total_frames <= 0:
        raise Exception("Could not read animation")

    frames = []

    indexes = [
        int(i * total_frames / frame_count)
        for i in range(frame_count)
    ]

    for index in indexes:
        cap.set(cv2.CAP_PROP_POS_FRAMES, index)

        success, frame = cap.read()

        if success:
            frame = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            image = Image.fromarray(frame)

            output = io.BytesIO()
            image.save(
                output,
                format="JPEG",
                quality=80
            )

            output.seek(0)

            frames.append(output)

    cap.release()

    return frames

