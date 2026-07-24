def analyze_prescription(ocr_text):
    return f"""
Analyze this medical prescription.

Tasks:
- Extract medicine names.
- Extract dosage and instructions if visible.
- Identify drug forms (tablet, capsule, injection, syrup, etc.).
- Explain the general purpose of each medicine.
- Explain abbreviations used in prescriptions.
- Organize the prescription information clearly.

Important:
- This is educational information only.
- Do not change dosage or provide medical treatment advice.
- If text is unclear, mention uncertainty.

Prescription text:
{ocr_text}
"""
