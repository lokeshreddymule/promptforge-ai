from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from utils.helpers import load_template


def rewrite_prompt(
    original_prompt: str,
    prompt_type: str,
    llm: ChatOpenAI,
    analysis_summary: str = "",
) -> str:
    """Rewrite a prompt to improve clarity, context, and structure."""
    try:
        template = load_template("rewrite_template.txt")
        rewrite_prompt_text = template.format(
            prompt=original_prompt,
            prompt_type=prompt_type,
        )

        if analysis_summary:
            rewrite_prompt_text += f"\n\nAnalysis issues to fix:\n{analysis_summary}"

        messages = [HumanMessage(content=rewrite_prompt_text)]
        response = llm.invoke(messages)
        return response.content.strip()

    except Exception as e:
        return f"Error rewriting prompt: {str(e)}"


def self_refine_prompt(
    original_prompt: str,
    prompt_type: str,
    llm: ChatOpenAI,
    iterations: int = 2,
) -> tuple[str, list]:
    """
    Self-refine prompt through multiple iterations.
    Returns (final_prompt, history_of_versions)
    """
    history = [original_prompt]
    current_prompt = original_prompt

    for i in range(iterations):
        refined = rewrite_prompt(current_prompt, prompt_type, llm)
        history.append(refined)
        current_prompt = refined

    return current_prompt, history
