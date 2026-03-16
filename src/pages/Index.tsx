import { useState, useCallback } from "react";
import ParticleField from "@/components/ParticleField";
import HeroSection from "@/components/HeroSection";
import InputArena, { type ForgeSettings } from "@/components/InputArena";
import PipelineVisualization from "@/components/PipelineVisualization";
import ResultsBento, { type ForgeResult } from "@/components/ResultsBento";
import AnalyticsDashboard from "@/components/AnalyticsDashboard";
import PromptHistory from "@/components/PromptHistory";

export interface HistoryEntry {
  id: number;
  timestamp: string;
  promptType: string;
  originalPrompt: string;
  optimizedPrompt: string;
  originalScore: number;
  optimizedScore: number;
  improvement: number;
}

const Index = () => {
  const [isProcessing, setIsProcessing] = useState(false);
  const [pipelineStep, setPipelineStep] = useState(-1);
  const [result, setResult] = useState<ForgeResult | null>(null);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [apiKey, setApiKey] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleForge = useCallback(async (prompt: string, settings: ForgeSettings) => {
    setIsProcessing(true);
    setResult(null);
    setError(null);
    setPipelineStep(0);

    const stepInterval = setInterval(() => {
      setPipelineStep((prev) => {
        if (prev < 5) return prev + 1;
        return prev;
      });
    }, 800);

    try {
      const response = await fetch("http://localhost:8501/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt,
          model: settings.model,
          temperature: settings.temperature,
          self_refine: settings.selfRefine,
          save_memory: settings.saveMemory,
          api_key: apiKey,
        }),
      });

      clearInterval(stepInterval);

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();
      setPipelineStep(6);

      const forgeResult: ForgeResult = {
        detectedType: data.prompt_type || "General",
        problems: data.analysis?.problems || ["Vague instructions", "No output format"],
        improvements: data.analysis?.suggestions || ["Added role", "Defined output format"],
        originalPrompt: prompt,
        optimizedPrompt: data.optimized_prompt || prompt,
        scores: {
          clarity: data.optimized_score?.clarity || 8.0,
          specificity: data.optimized_score?.specificity || 8.0,
          context: data.optimized_score?.context || 7.5,
          structure: data.optimized_score?.structure || 8.5,
        },
        originalScores: {
          clarity: data.original_score?.clarity || 4.0,
          specificity: data.original_score?.specificity || 3.0,
          context: data.original_score?.context || 3.0,
          structure: data.original_score?.structure || 4.0,
        },
        improvement: Math.round(data.improvement_pct || 128),
        criticVerdict: data.critique?.approved ? "APPROVED" : "NEEDS_REVISION",
        criticFeedback: [
          { label: "Clarity", text: data.critique?.clarity_feedback || "Good" },
          { label: "Specificity", text: data.critique?.specificity_feedback || "Improved" },
          { label: "Context", text: data.critique?.context_feedback || "Context added" },
          { label: "Structure", text: data.critique?.structure_feedback || "Well structured" },
          { label: "Output Format", text: data.critique?.output_format_feedback || "Format specified" },
          { label: "Top Suggestion", text: data.critique?.top_suggestion || "Consider adding examples" },
        ],
        originalResponse: data.original_response || "No response generated",
        optimizedResponse: data.optimized_response || "No response generated",
        originalScore: data.original_score?.total || 3.5,
        optimizedScore: data.optimized_score?.total || 8.0,
      };

      setTimeout(() => {
        setResult(forgeResult);
        setIsProcessing(false);
        const entry: HistoryEntry = {
          id: Date.now(),
          timestamp: new Date().toLocaleString(),
          promptType: forgeResult.detectedType,
          originalPrompt: prompt,
          optimizedPrompt: forgeResult.optimizedPrompt,
          originalScore: forgeResult.originalScore,
          optimizedScore: forgeResult.optimizedScore,
          improvement: forgeResult.improvement,
        };
        setHistory((prev) => [entry, ...prev].slice(0, 20));
      }, 500);

    } catch (err: any) {
      clearInterval(stepInterval);
      setIsProcessing(false);
      setPipelineStep(-1);

      if (err.message.includes("fetch") || err.message.includes("Failed")) {
        setError("⚠️ Backend not connected. Running in DEMO MODE. Start your Python backend to get real results.");
        const demoResult: ForgeResult = {
          detectedType: "General",
          problems: ["Vague instructions", "No output format", "Missing context"],
          improvements: ["Added role definition", "Defined output format", "Added context", "Set constraints"],
          originalPrompt: prompt,
          optimizedPrompt: `You are an expert assistant specializing in clear, comprehensive explanations.\n\nTask: ${prompt}\n\nRequirements:\n- Provide a detailed, well-structured response\n- Use clear headings and bullet points where appropriate\n- Include practical examples\n- Target audience: intermediate learner\n\nOutput Format: Structured explanation with sections`,
          scores: { clarity: 8.5, specificity: 8.0, context: 7.5, structure: 9.0 },
          originalScores: { clarity: 4.0, specificity: 3.0, context: 3.0, structure: 4.0 },
          improvement: 128,
          criticVerdict: "APPROVED",
          criticFeedback: [
            { label: "Clarity", text: "Clear role and task definition" },
            { label: "Specificity", text: "Specific requirements added" },
            { label: "Context", text: "Target audience specified" },
            { label: "Structure", text: "Well organized with sections" },
            { label: "Output Format", text: "Format explicitly defined" },
            { label: "Top Suggestion", text: "Consider adding examples" },
          ],
          originalResponse: "This is a demo response for the original prompt. Connect your Python backend for real AI responses.",
          optimizedResponse: "This is a demo response for the optimized prompt. The optimized version would get significantly better results from any AI model. Connect your Python backend to see the real difference!",
          originalScore: 3.5,
          optimizedScore: 8.0,
        };
        setPipelineStep(6);
        setTimeout(() => { setResult(demoResult); }, 500);
      } else {
        setError(`Error: ${err.message}`);
      }
    }
  }, [apiKey]);

  return (
    <div className="relative min-h-screen bg-background">
      <div className="grain-overlay" />
      <ParticleField />

      <HeroSection />

      {error && (
        <div className="relative z-20 max-w-4xl mx-auto px-4 mb-4">
          <div className="glass-card p-4 border-l-2 border-l-neon-gold">
            <p className="text-sm font-mono text-neon-gold">{error}</p>
          </div>
        </div>
      )}

      <InputArena
        onForge={handleForge}
        isProcessing={isProcessing}
        apiKey={apiKey}
        onApiKeyChange={setApiKey}
      />

      {pipelineStep >= 0 && <PipelineVisualization activeStep={pipelineStep} />}

      {result && <ResultsBento result={result} />}

      {history.length > 0 && (
        <>
          <AnalyticsDashboard history={history} />
          <PromptHistory history={history} onClear={() => setHistory([])} />
        </>
      )}

      <footer className="relative z-20 py-10 text-center border-t border-border">
        <p style={{ fontFamily: "monospace", fontSize: "0.95rem", color: "#a5b4fc", fontWeight: "600" }}>
          Built by Lokesh Reddy
        </p>
        <p style={{ fontFamily: "monospace", fontSize: "0.75rem", color: "#475569", marginTop: "6px" }}>
          PromptForge AI — AI Prompt Optimization System
        </p>
      </footer>
    </div>
  );
};

export default Index;
