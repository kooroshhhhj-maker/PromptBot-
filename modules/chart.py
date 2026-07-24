def analyze_chart(ocr_text):
    return f"""
Analyze this chart, graph, or table.

Tasks:
- Identify the chart type.
- Explain what the axes represent.
- Extract visible values and labels.
- Summarize the trend.
- Compare important data points.
- Explain increases, decreases, or patterns.
- If it is a scientific chart, explain its meaning.

Chart text:
{ocr_text}
"""

