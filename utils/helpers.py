import json
import re
import os
from pathlib import Path


def load_template(template_name: str) -> str:
    """Load a prompt template from the prompts directory."""
    base_dir = Path(__file__).parent.parent
    template_path = base_dir / "prompts" / template_name
    with open(template_path, "r") as f:
        return f.read()


def safe_json_parse(text: str) -> dict:
    """Safely parse JSON from LLM response, handling markdown code blocks."""
    # Remove markdown code blocks if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to extract JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}


def count_tokens_approx(text: str) -> int:
    """Approximate token count (1 token ≈ 4 characters)."""
    return len(text) // 4


def calculate_improvement_percentage(original_score: float, optimized_score: float) -> float:
    """Calculate improvement percentage between two scores."""
    if original_score == 0:
        return 100.0
    return round(((optimized_score - original_score) / original_score) * 100, 1)


def format_score_display(score: float) -> str:
    """Format score for display."""
    if score >= 8:
        return f"🟢 {score}/10"
    elif score >= 6:
        return f"🟡 {score}/10"
    else:
        return f"🔴 {score}/10"


def get_quality_label(score: float) -> str:
    """Get quality label based on score."""
    if score >= 8.5:
        return "Excellent"
    elif score >= 7:
        return "Good"
    elif score >= 5:
        return "Fair"
    else:
        return "Poor"
