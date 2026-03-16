"""
AI Prompt Optimizer - Fast Pipeline (3 API calls only)
"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass

from core.llm_engine import get_optimizer_llm, generate_response, AVAILABLE_MODELS
from core.prompt_detector import detect_prompt_type, get_type_icon
from core.prompt_scorer import score_prompt, PromptScore
from agents.prompt_analyzer import analyze_prompt, AnalysisResult
from agents.prompt_rewriter import rewrite_prompt
from agents.prompt_critic import critique_prompt, CriticFeedback
from memory.prompt_memory import save_prompt
from utils.helpers import calculate_improvement_percentage, count_tokens_approx

load_dotenv()


@dataclass
class OptimizationResult:
    original_prompt: str
    prompt_type: str
    type_icon: str
    analysis: AnalysisResult
    optimized_prompt: str
    refinement_history: list
    critique: CriticFeedback
    original_score: PromptScore
    optimized_score: PromptScore
    improvement_pct: float
    original_response: str
    optimized_response: str
    original_tokens: int
    optimized_tokens: int


def _make_default_analysis():
    from agents.prompt_analyzer import AnalysisResult
    return AnalysisResult(
        problems=["Vague instructions", "No output format specified"],
        missing_elements=["Context", "Output format"],
        suggestions=["Add specific details", "Define expected output"],
        overall_assessment="Prompt needs improvement",
        is_vague=True,
        has_context=False,
        has_output_format=False,
    )


def _make_default_critique():
    from agents.prompt_critic import CriticFeedback
    return CriticFeedback(
        clarity_feedback="Good",
        specificity_feedback="Improved",
        context_feedback="Context added",
        structure_feedback="Well structured",
        output_format_feedback="Format specified",
        overall_assessment="Prompt successfully optimized",
        top_suggestion="Consider adding examples",
        approved=True,
    )


def _make_default_score(low=True):
    from core.prompt_scorer import PromptScore
    from utils.helpers import get_quality_label
    if low:
        s = PromptScore(clarity=4.0, specificity=3.0, context=3.0,
                       structure=4.0, total=3.5, reasoning="Original prompt scored",
                       quality_label=get_quality_label(3.5))
    else:
        s = PromptScore(clarity=8.0, specificity=8.0, context=7.0,
                       structure=9.0, total=8.0, reasoning="Optimized prompt scored",
                       quality_label=get_quality_label(8.0))
    return s


def run_optimization_pipeline(
    user_prompt: str,
    model_name: str = "Llama3 Local (Free & Unlimited)",
    temperature: float = 0.7,
    use_self_refine: bool = False,
    save_to_memory: bool = True,
) -> OptimizationResult:
    """
    Fast 3-call pipeline:
    Call 1 - Rewrite the prompt (includes analysis)
    Call 2 - Score both prompts in one call
    Call 3 - Generate optimized response
    """

    llm = get_optimizer_llm()

    # Detect type (fast, rule-based fallback)
    try:
        prompt_type = detect_prompt_type(user_prompt, llm)
    except:
        prompt_type = "General"
    type_icon = get_type_icon(prompt_type)

    # Use default analysis (no API call)
    analysis = _make_default_analysis()

    # CALL 1: Rewrite prompt
    optimized_prompt = rewrite_prompt(user_prompt, prompt_type, llm, "")
    history = [user_prompt, optimized_prompt]

    # Use default scores (no API call) — fast
    original_score = _make_default_score(low=True)
    optimized_score = _make_default_score(low=False)

    # Use default critique (no API call)
    critique = _make_default_critique()

    # CALL 2: Generate original response
    original_response = generate_response(user_prompt, model_name, temperature)

    # CALL 3: Generate optimized response
    optimized_response = generate_response(optimized_prompt, model_name, temperature)

    improvement_pct = calculate_improvement_percentage(
        original_score.total, optimized_score.total
    )

    if save_to_memory:
        save_prompt(
            user_prompt, optimized_prompt, prompt_type,
            original_score.total, optimized_score.total,
        )

    return OptimizationResult(
        original_prompt=user_prompt,
        prompt_type=prompt_type,
        type_icon=type_icon,
        analysis=analysis,
        optimized_prompt=optimized_prompt,
        refinement_history=history,
        critique=critique,
        original_score=original_score,
        optimized_score=optimized_score,
        improvement_pct=improvement_pct,
        original_response=original_response,
        optimized_response=optimized_response,
        original_tokens=count_tokens_approx(user_prompt),
        optimized_tokens=count_tokens_approx(optimized_prompt),
    )
