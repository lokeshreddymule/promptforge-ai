from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
import os


PROMPT_CATEGORIES = [
    "Coding",
    "Writing",
    "Research",
    "Explanation",
    "Summarization",
    "Analysis",
    "Creative",
    "Question & Answer",
    "Data & Math",
    "Brainstorming",
]

SYSTEM_PROMPT = """You are a prompt type classifier. Classify the user's prompt into exactly ONE of these categories:
- Coding
- Writing
- Research
- Explanation
- Summarization
- Analysis
- Creative
- Question & Answer
- Data & Math
- Brainstorming

Respond with ONLY the category name, nothing else."""


def detect_prompt_type(prompt: str, llm: ChatOpenAI) -> str:
    """Detect the type/category of the given prompt."""
    try:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Classify this prompt: {prompt}"),
        ]
        response = llm.invoke(messages)
        detected = response.content.strip()

        # Validate response
        for category in PROMPT_CATEGORIES:
            if category.lower() in detected.lower():
                return category

        return "General"
    except Exception as e:
        return "General"


def get_type_icon(prompt_type: str) -> str:
    """Get an icon for the prompt type."""
    icons = {
        "Coding": "💻",
        "Writing": "✍️",
        "Research": "🔬",
        "Explanation": "💡",
        "Summarization": "📝",
        "Analysis": "📊",
        "Creative": "🎨",
        "Question & Answer": "❓",
        "Data & Math": "🔢",
        "Brainstorming": "🧠",
        "General": "🔮",
    }
    return icons.get(prompt_type, "🔮")
