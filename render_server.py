"""
Render Server — serves both React frontend and Python API
Single server for everything on Render
"""

import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="PromptForge AI")

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


@app.get("/api/health")
def health():
    return {"status": "PromptForge AI running", "version": "1.0"}


@app.post("/optimize")
async def optimize(req: OptimizeRequest):
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


# Serve React frontend static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(static_dir / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        return FileResponse(str(static_dir / "index.html"))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting PromptForge AI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
