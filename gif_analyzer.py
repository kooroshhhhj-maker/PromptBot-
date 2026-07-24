import io
import cv2
from PIL import Image


def extract_gif_frame(video_bytes):
    video_path = "/tmp/gif.mp4"

    with open(video_path, "wb") as f:
        f.write(video_bytes)

    cap = cv2.VideoCapture(video_path)

    success, frame = cap.read()

    cap.release()

    if not success:
        raise Exception("Could not read animation")

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    image = Image.fromarray(frame)

    output = io.BytesIO()
    image.save(output, format="JPEG")
    output.seek(0)

    return output

