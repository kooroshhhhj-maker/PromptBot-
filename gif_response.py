from ai_client import ask_ai


def make_gif_reply(analysis):

    response = ask_ai([
        {
            "role": "system",
            "content": """
تو یک دوست باحال هستی.
کاربر یک GIF فرستاده و این تحلیل خام آن است.
از این تحلیل یک جواب طبیعی، کوتاه و دوستانه بساز.
فقط تحلیل خشک نده.
اگر GIF خنده‌دار بود شوخی کن.
اگر مفهوم خاصی داشت بگو.
حداکثر 3 جمله جواب بده.
"""
        },
        {
            "role": "user",
            "content": analysis
        }
    ])

    return response

