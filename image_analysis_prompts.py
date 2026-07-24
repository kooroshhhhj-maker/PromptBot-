ANALYSIS_PROMPTS = {
    "microscope": """
Analyze this image as a microscope image.
Focus on:
- cells
- bacteria
- parasites
- staining patterns
- morphology
- possible laboratory interpretation
Do not invent results. Mention uncertainty.
""",

    "laboratory": """
Analyze this as a laboratory-related image.
Focus on:
- instruments
- samples
- tests
- labels
- possible procedures
Explain professionally.
""",

    "prescription": """
Analyze this as a medical prescription or document.
Focus on:
- medication names
- handwriting
- dosage
- instructions
Warn if text is unclear.
""",

    "document": """
Analyze this document image.
Focus on:
- extracting text
- important information
- structure
- summary.
""",

    "chart": """
Analyze this chart or graph.
Focus on:
- axes
- values
- trends
- interpretation.
""",

    "general": """
Analyze this image carefully and describe important details.
"""
}


def get_analysis_prompt(image_type):
    return ANALYSIS_PROMPTS.get(
        image_type,
        ANALYSIS_PROMPTS["general"]
    )

