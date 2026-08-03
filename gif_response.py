from ai_client import ask_ai


def make_gif_reply(analysis):
    print("GIF RESPONSE INPUT:")
    print(analysis)
    print("==============")
    print("GIF ANALYSIS:")
    print(analysis)
    print("==============")
    print("GIF ANALYSIS SENT TO AI:")
    print(analysis)
    response = ask_ai([
        {
            "role": "system",
            "content":"""
You are a GIF analysis assistant.
Based only on the provided analysis, write a short answer.
Do not invent anything.
Do not greet.
Do not ask questions.
Maximum 2 sentences.
""" 

        },
        {
            "role": "user",
            "content": analysis
        }
    ])

    return response

