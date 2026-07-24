def analyze_document(ocr_text):
    return f"""
Analyze this document.

Tasks:
- Identify the document type.
- Summarize the main content.
- Extract important information.
- Explain difficult sections.
- Find dates, names, numbers, and important fields.
- Organize the information clearly.
- If it is a form, explain each field.
- If it is an academic document, extract key points.

Document text:
{ocr_text}
"""

