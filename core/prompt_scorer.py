from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from utils.helpers import load_template, safe_json_parse, get_quality_label
from dataclasses import dataclass


@dataclass
class PromptScore:
    clarity: float
    specificity: float
    context: float
    structure: float
    total: float
    reasoning: str
    quality_label: str

    def to_dict(self) -> dict:
        return {
            "clarity": self.clarity,
            "specificity": self.specificity,
            "context": self.context,
            "structure": self.structure,
            "total": self.total,
            "reasoning": self.reasoning,
            "quality_label": self.quality_label,
        }


def score_prompt(prompt: str, llm: ChatOpenAI) -> PromptScore:
    """Score a prompt across multiple dimensions."""
    try:
        template = load_template("scoring_template.txt")
        scoring_prompt = template.format(prompt=prompt)

        messages = [HumanMessage(content=scoring_prompt)]
        response = llm.invoke(messages)

        data = safe_json_parse(response.content)

        clarity = float(data.get("clarity", 5))
        specificity = float(data.get("specificity", 5))
        context = float(data.get("context", 5))
        structure = float(data.get("structure", 5))
        total = round((clarity + specificity + context + structure) / 4, 1)
        reasoning = data.get("reasoning", "Score calculated based on prompt analysis.")

        return PromptScore(
            clarity=clarity,
            specificity=specificity,
            context=context,
            structure=structure,
            total=total,
            reasoning=reasoning,
            quality_label=get_quality_label(total),
        )
    except Exception as e:
        # Return default scores on error
        return PromptScore(
            clarity=4.0,
            specificity=3.0,
            context=3.0,
            structure=4.0,
            total=3.5,
            reasoning="Unable to score prompt automatically.",
            quality_label="Fair",
        )
