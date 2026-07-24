def analyze_laboratory(ocr_text):
    return f"""
Analyze this laboratory-related image or report.

Possible categories:
- Blood tests (CBC, biochemistry, hormones)
- Microbiology (culture, antibiogram, staining)
- Molecular tests (PCR, RT-PCR)
- Immunology tests (ELISA, antibodies, antigens)
- Pathology reports
- Microscopy images
- Parasitology reports
- Veterinary laboratory tests

Tasks:
- Extract all visible laboratory information.
- Explain abbreviations.
- Organize results clearly.
- Highlight abnormal values if present.
- Explain the purpose of each test.
- Provide educational interpretation.
- Do not give a definitive medical diagnosis.

Laboratory text:
{ocr_text}
"""

