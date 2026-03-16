from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.helpers import safe_json_parse
from dataclasses import dataclass, field
from typing import List


@dataclass
class AnalysisResult:
    problems: List[str]
    missing_elements: List[str]
    suggestions: List[str]
    overall_assessment: str
    is_vague: bool
    has_context: bool
    has_output_format: bool

    def to_dict(self) -> dict:
        return {
            "problems": self.problems,
            "missing_elements": self.missing_elements,
            "suggestions": self.suggestions,
            "overall_assessment": self.overall_assessment,
            "is_vague": self.is_vague,
            "has_context": self.has_context,
            "has_output_format": self.has_output_format,
        }


ANALYZER_SYSTEM = """You are an expert prompt analyst. Analyze prompts for quality issues.

Respond in this EXACT JSON format:
{
  "problems": ["problem1", "problem2"],
  "missing_elements": ["element1", "element2"],
  "suggestions": ["suggestion1", "suggestion2"],
  "overall_assessment": "brief assessment",
  "is_vague": true or false,
  "has_context": true or false,
  "has_output_format": true or false
}"""


def analyze_prompt(prompt: str, llm: ChatOpenAI) -> AnalysisResult:
    """Analyze a prompt for quality issues and missing elements."""
    try:
        user_message = f"""Analyze this prompt for quality issues:

"{prompt}"

Check for:
1. Vague or ambiguous instructions
2. Missing context or background
3. Unclear task definition
4. Missing output format specification
5. Missing constraints or quality criteria"""

        messages = [
            SystemMessage(content=ANALYZER_SYSTEM),
            HumanMessage(content=user_message),
        ]
        response = llm.invoke(messages)
        data = safe_json_parse(response.content)

        return AnalysisResult(
            problems=data.get("problems", ["Prompt needs improvement"]),
            missing_elements=data.get("missing_elements", ["Output format", "Context"]),
            suggestions=data.get("suggestions", ["Add more specificity"]),
            overall_assessment=data.get("overall_assessment", "Prompt analyzed"),
            is_vague=data.get("is_vague", True),
            has_context=data.get("has_context", False),
            has_output_format=data.get("has_output_format", False),
        )
    except Exception as e:
        return AnalysisResult(
            problems=["Could not fully analyze prompt"],
            missing_elements=["Context", "Output format"],
            suggestions=["Add more detail and specificity"],
            overall_assessment="Basic analysis completed",
            is_vague=True,
            has_context=False,
            has_output_format=False,
        )
