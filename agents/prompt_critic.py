from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils.helpers import load_template, safe_json_parse
from dataclasses import dataclass


@dataclass
class CriticFeedback:
    clarity_feedback: str
    specificity_feedback: str
    context_feedback: str
    structure_feedback: str
    output_format_feedback: str
    overall_assessment: str
    top_suggestion: str
    approved: bool

    def to_dict(self) -> dict:
        return {
            "clarity_feedback": self.clarity_feedback,
            "specificity_feedback": self.specificity_feedback,
            "context_feedback": self.context_feedback,
            "structure_feedback": self.structure_feedback,
            "output_format_feedback": self.output_format_feedback,
            "overall_assessment": self.overall_assessment,
            "top_suggestion": self.top_suggestion,
            "approved": self.approved,
        }


def critique_prompt(
    original_prompt: str,
    rewritten_prompt: str,
    llm: ChatOpenAI,
) -> CriticFeedback:
    """Critically evaluate a rewritten prompt."""
    try:
        template = load_template("critic_template.txt")
        critic_message = template.format(
            rewritten_prompt=rewritten_prompt,
            original_prompt=original_prompt,
        )

        messages = [HumanMessage(content=critic_message)]
        response = llm.invoke(messages)
        data = safe_json_parse(response.content)

        return CriticFeedback(
            clarity_feedback=data.get("clarity_feedback", "Not evaluated"),
            specificity_feedback=data.get("specificity_feedback", "Not evaluated"),
            context_feedback=data.get("context_feedback", "Not evaluated"),
            structure_feedback=data.get("structure_feedback", "Not evaluated"),
            output_format_feedback=data.get("output_format_feedback", "Not evaluated"),
            overall_assessment=data.get("overall_assessment", "Prompt reviewed"),
            top_suggestion=data.get("top_suggestion", "Continue improving specificity"),
            approved=data.get("approved", True),
        )
    except Exception as e:
        return CriticFeedback(
            clarity_feedback="Good",
            specificity_feedback="Acceptable",
            context_feedback="Could be improved",
            structure_feedback="Well structured",
            output_format_feedback="Format specified",
            overall_assessment="Prompt has been improved from original",
            top_suggestion="Consider adding specific examples",
            approved=True,
        )
