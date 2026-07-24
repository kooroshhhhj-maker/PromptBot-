def analyze_formula(ocr_text):
    return f"""
Analyze this formula, equation, or scientific expression.

Tasks:
- Identify the formula or equation.
- Explain what each symbol means.
- Identify the field (math, physics, chemistry, biology, laboratory science, statistics).
- Explain when this formula is used.
- Describe the relationship between variables.
- If numerical values are provided, show how to solve it step by step.
- Explain the result in a simple educational way.

Formula or text:
{ocr_text}
"""

