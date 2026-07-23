import io
from PIL import Image


def extract_gif_frame(gif_bytes):
    gif = Image.open(io.BytesIO(gif_bytes))

    gif.seek(0)

    frame = gif.convert("RGB")

    output = io.BytesIO()
    frame.save(output, format="JPEG")
    output.seek(0)

    return output

