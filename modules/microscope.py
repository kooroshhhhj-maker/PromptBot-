def analyze_microscope(ocr_text):
    return f"""
Analyze this microscopy image or laboratory microscopy report.

Possible categories:
- Bacteria
- Fungi
- Parasites
- Blood cells
- Histology and tissues
- Microorganisms
- Laboratory slides

Tasks:
- Describe visible structures.
- Identify possible biological category if possible.
- Explain important features.
- Explain staining or microscopy methods if mentioned.
- Provide educational background.
- Mention uncertainty when identification is not clear.

Important:
- Do not provide a definitive clinical diagnosis.
- This is educational microscopy analysis.

Microscopy information:
{ocr_text}
"""

