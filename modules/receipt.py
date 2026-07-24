def analyze_receipt(ocr_text):
    return f"""
Analyze this receipt or invoice.

Tasks:
- Extract store name if available.
- Extract all products and prices.
- Find total amount.
- Find date and time if available.
- Summarize the purchase.

Receipt text:
{ocr_text}
"""

