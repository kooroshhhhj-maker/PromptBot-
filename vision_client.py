import requests
import base64


ANALYSIS_PROMPTS = {
    "microscope": (
        "You are an expert biomedical image analyst. "
        "Analyze this microscopy image professionally. "
        "Focus on specimen morphology, possible cells or microorganisms, "
        "staining patterns, structures, image quality, and scientific interpretation. "
        "Do not make a definitive diagnosis. Mention uncertainty."
    ),

    "laboratory": (
        "You are a laboratory science expert. "
        "Analyze this laboratory image. "
        "Identify equipment, samples, procedures, and scientific context. "
        "Provide a professional laboratory report."
    ),

    "prescription": (
        "You are a medical document analysis assistant. "
        "Read this prescription image. "
        "Extract visible text, medication names, dosage information, "
        "and mention unclear parts. Do not invent information."
    ),

    "document": (
        "You are an OCR and document analysis expert. "
        "Extract all visible text and organize the document information clearly."
    ),

    "chart": (
        "You are a scientific data analyst. "
        "Analyze this chart, identify trends, values, labels, and conclusions."
    ),

    "general": (
        "Analyze this image in detail. "
        "Describe objects, scene, and read any visible text."
     ),
  
  "prompt_generator": (
    "You are an expert AI prompt engineer. "
    "Analyze this image and create one professional image generation prompt. "
    "Describe the subject, composition, lighting, camera angle, colours, "
    "style, materials, background and quality. "
    "Return ONLY the final prompt."
  )
}


def analyze_image(image_bytes, token, account_id, analysis_type="general"):

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    image_data_uri = f"data:image/jpeg;base64,{image_base64}"

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/@cf/meta/llama-3.2-11b-vision-instruct"
    )

    prompt = ANALYSIS_PROMPTS.get(
        analysis_type,
        ANALYSIS_PROMPTS["general"]
    )

    payload = {
        "image": image_data_uri,
        "prompt": prompt
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=120
    )

    print("CLOUDFLARE STATUS:", response.status_code)
    print(response.json())
    print("RAW JSON:")   
    print("PAYLOAD SENT:", payload.keys())
    print("IMAGE SIZE:", len(image_bytes))
    print(response.json())

    if response.status_code != 200:
        return None

    data = response.json()

    result = data.get("result")

    print("VISION RESULT TYPE:", type(result))
    print("VISION RESULT:", result)

    if isinstance(result, dict):
        return (
            result.get("response")
            print("RAW JSON:")
	    print(response.text)
            or result.get("description")
            or str(result)
        )

    return str(result)
