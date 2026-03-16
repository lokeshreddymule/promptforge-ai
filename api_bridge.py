"""
FastAPI Bridge — connects React frontend to Python backend
Run this alongside your Streamlit app:
  python api_bridge.py
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="PromptForge AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class OptimizeRequest(BaseModel):
    prompt: str
    model: str = "Groq - Llama3.1 8B (Free)"
    temperature: float = 0.7
    self_refine: bool = False
    save_memory: bool = True
    api_key: str = ""


@app.get("/")
def root():
    return {"status": "PromptForge AI API running", "version": "1.0"}


@app.post("/optimize")
async def optimize(req: OptimizeRequest):
    # Set API key if provided
    if req.api_key:
        if req.api_key.startswith("gsk_"):
            os.environ["GROQ_API_KEY"] = req.api_key
        elif req.api_key.startswith("AIza"):
            os.environ["GOOGLE_API_KEY"] = req.api_key
        elif req.api_key.startswith("sk-"):
            os.environ["OPENAI_API_KEY"] = req.api_key

    from app import run_optimization_pipeline
    result = run_optimization_pipeline(
        user_prompt=req.prompt,
        model_name=req.model,
        temperature=req.temperature,
        use_self_refine=req.self_refine,
        save_to_memory=req.save_memory,
    )

    return {
        "prompt_type": result.prompt_type,
        "type_icon": result.type_icon,
        "analysis": result.analysis.to_dict(),
        "optimized_prompt": result.optimized_prompt,
        "original_score": result.original_score.to_dict(),
        "optimized_score": result.optimized_score.to_dict(),
        "improvement_pct": result.improvement_pct,
        "critique": result.critique.to_dict(),
        "original_response": result.original_response,
        "optimized_response": result.optimized_response,
        "original_tokens": result.original_tokens,
        "optimized_tokens": result.optimized_tokens,
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting PromptForge AI API on http://localhost:8501/optimize")
    uvicorn.run(app, host="0.0.0.0", port=8501)
