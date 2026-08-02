import os
import tempfile
import subprocess


def extract_gif_frames(file_bytes, max_frames=5):
    try:
        temp_input = tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=False
        )

        temp_input.write(file_bytes)
        temp_input.close()

        temp_dir = tempfile.mkdtemp()

        output_pattern = os.path.join(
            temp_dir,
            "frame_%03d.jpg"
        )

        command = [
            "ffmpeg",
            "-i",
            temp_input.name,
            "-vf",
            "fps=1",
            "-frames:v",
            str(max_frames),
            output_pattern,
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        print("FFMPEG RETURN:", result.returncode)
        print(result.stderr.decode())

        output_frames = []

        for filename in sorted(os.listdir(temp_dir)):
            if filename.endswith(".jpg"):
                path = os.path.join(temp_dir, filename)

                with open(path, "rb") as f:
                    frame = f.read()
                    output_frames.append(frame)

        print("GIF FRAMES:", len(output_frames))

        for i, frame in enumerate(output_frames):
            print(
                "FRAME",
                i,
                "SIZE:",
                len(frame)
            )

        os.unlink(temp_input.name)

        return output_frames

    except Exception as e:
        print("GIF ERROR:", e)
        return []
