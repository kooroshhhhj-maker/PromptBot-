def save_user_image(user_id, image_bytes):
    path = f"user_{user_id}.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    return path


def edit_image(image_path, prompt):
    print("Image editing temporarily unavailable")
    return None
