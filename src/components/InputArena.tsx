import { useState, useRef } from "react";
import { Zap, Key } from "lucide-react";

interface InputArenaProps {
  onForge: (prompt: string, settings: ForgeSettings) => void;
  isProcessing: boolean;
  apiKey: string;
  onApiKeyChange: (key: string) => void;
}

export interface ForgeSettings {
  model: string;
  temperature: number;
  selfRefine: boolean;
  saveMemory: boolean;
}

const MODELS = [
  { id: "Groq - Llama3.1 8B (Free)", label: "Llama 3.1 8B", provider: "Groq", color: "bg-neon-cyan" },
  { id: "Groq - Llama3.3 70B (Free)", label: "Llama 3.3 70B", provider: "Groq", color: "bg-neon-cyan" },
  { id: "Groq - Gemma2 9B (Free)", label: "Gemma2 9B", provider: "Groq", color: "bg-neon-cyan" },
  { id: "Gemini 2.0 Flash (Free)", label: "Gemini 2.0 Flash", provider: "Google", color: "bg-neon-green" },
  { id: "Gemini 1.5 Flash (Free)", label: "Gemini 1.5 Flash", provider: "Google", color: "bg-neon-green" },
  { id: "Llama3 Local (Ollama)", label: "Llama3 Local", provider: "Ollama", color: "bg-neon-violet" },
  { id: "OpenAI GPT-4o Mini", label: "GPT-4o Mini", provider: "OpenAI", color: "bg-neon-gold" },
];

const EXAMPLES = [
  "Explain AI and machine learning",
  "Write Python code for binary search",
  "Write a blog about future of technology",
  "Summarize the impact of climate change",
];

const InputArena = ({ onForge, isProcessing, apiKey, onApiKeyChange }: InputArenaProps) => {
  const [prompt, setPrompt] = useState("");
  const [model, setModel] = useState(MODELS[0].id);
  const [temperature, setTemperature] = useState(0.7);
  const [selfRefine, setSelfRefine] = useState(false);
  const [saveMemory, setSaveMemory] = useState(true);
  const [showModels, setShowModels] = useState(false);
  const [showApiKey, setShowApiKey] = useState(false);
  const btnRef = useRef<HTMLButtonElement>(null);

  const selectedModel = MODELS.find((m) => m.id === model) || MODELS[0];
  const maxChars = 2000;

  const handleForge = () => {
    if (!prompt.trim() || isProcessing) return;
    if (btnRef.current) {
      const ripple = document.createElement("span");
      ripple.className = "absolute rounded-full bg-primary-foreground/30";
      ripple.style.width = ripple.style.height = "20px";
      ripple.style.animation = "ripple 0.6s ease-out forwards";
      const rect = btnRef.current.getBoundingClientRect();
      ripple.style.left = `${rect.width / 2 - 10}px`;
      ripple.style.top = `${rect.height / 2 - 10}px`;
      btnRef.current.appendChild(ripple);
      setTimeout(() => ripple.remove(), 600);
    }
    onForge(prompt, { model, temperature, selfRefine, saveMemory });
  };

  const charPercent = prompt.length / maxChars;

  return (
    <section className="relative z-20 max-w-4xl mx-auto px-4 py-20" id="input">
      <h2 className="font-display text-3xl sm:text-4xl font-bold mb-2 text-center gradient-text-primary">
        Input Arena
      </h2>
      <p className="text-muted-foreground text-center mb-10 text-sm">
        Drop your raw prompt below and watch the magic happen
      </p>

      <div className="glass-card p-6 sm:p-8 space-y-6">

        {/* Quick Examples */}
        <div>
          <p className="text-xs font-mono text-muted-foreground mb-2">QUICK EXAMPLES</p>
          <div className="flex flex-wrap gap-2">
            {EXAMPLES.map((ex, i) => (
              <button
                key={i}
                onClick={() => setPrompt(ex)}
                className="px-3 py-1 rounded-full text-xs font-mono border border-border hover:border-primary/50 hover:text-primary bg-background/40 text-muted-foreground transition-all"
              >
                {ex}
              </button>
            ))}
          </div>
        </div>

        {/* Textarea */}
        <div className="relative group">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value.slice(0, maxChars))}
            placeholder="Enter your raw prompt here..."
            rows={6}
            className="w-full bg-background/60 border border-border rounded-lg p-4 font-mono text-sm text-foreground placeholder:text-muted-foreground resize-none focus:outline-none focus:border-accent focus:shadow-[0_0_20px_hsl(186_100%_50%/0.15)] transition-all duration-300"
          />
          <div className="absolute bottom-3 right-3 flex items-center gap-2">
            <span className={`font-mono text-xs ${charPercent > 0.9 ? "text-destructive" : charPercent > 0.7 ? "text-neon-gold" : "text-muted-foreground"}`}>
              {prompt.length}/{maxChars}
            </span>
          </div>
        </div>

        {/* Controls row */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          {/* Model selector */}
          <div className="relative">
            <label className="text-xs text-muted-foreground mb-1.5 block font-mono">MODEL</label>
            <button
              onClick={() => setShowModels(!showModels)}
              className="w-full flex items-center justify-between px-4 py-2.5 rounded-lg border border-border bg-background/60 hover:border-primary/50 transition-colors"
            >
              <div className="flex items-center gap-2">
                <span className={`w-2 h-2 rounded-full ${selectedModel.color}`} />
                <span className="text-sm font-body">{selectedModel.label}</span>
              </div>
              <span className="text-xs text-muted-foreground">{selectedModel.provider}</span>
            </button>
            {showModels && (
              <div className="absolute top-full mt-1 w-full glass-card p-2 z-30">
                {MODELS.map((m) => (
                  <button
                    key={m.id}
                    onClick={() => { setModel(m.id); setShowModels(false); }}
                    className={`w-full flex items-center justify-between px-3 py-2 rounded-md text-sm hover:bg-muted/50 transition-colors ${m.id === model ? "bg-muted/30" : ""}`}
                  >
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${m.color}`} />
                      <span>{m.label}</span>
                    </div>
                    <span className="text-xs text-muted-foreground">{m.provider}</span>
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Temperature */}
          <div>
            <label className="text-xs text-muted-foreground mb-1.5 block font-mono">
              TEMPERATURE: {temperature.toFixed(1)}
            </label>
            <div className="relative px-1 py-3">
              <input
                type="range" min="0" max="1" step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full h-1.5 rounded-full appearance-none cursor-pointer"
                style={{ background: `linear-gradient(to right, hsl(263 84% 58%) ${temperature * 100}%, hsl(245 30% 17%) ${temperature * 100}%)` }}
              />
            </div>
          </div>
        </div>

        {/* API Key */}
        <div>
          <button
            onClick={() => setShowApiKey(!showApiKey)}
            className="flex items-center gap-2 text-xs font-mono text-muted-foreground hover:text-primary transition-colors"
          >
            <Key className="w-3 h-3" />
            {showApiKey ? "HIDE API KEY" : "SET API KEY (optional — uses .env by default)"}
          </button>
          {showApiKey && (
            <input
              type="password"
              value={apiKey}
              onChange={(e) => onApiKeyChange(e.target.value)}
              placeholder="gsk_... or AIza... or sk-..."
              className="mt-2 w-full bg-background/60 border border-border rounded-lg px-4 py-2 font-mono text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-accent transition-all"
            />
          )}
        </div>

        {/* Toggles */}
        <div className="flex flex-wrap gap-6">
          {[
            { label: "Self-Refine", value: selfRefine, set: setSelfRefine },
            { label: "Save Memory", value: saveMemory, set: setSaveMemory },
          ].map(({ label, value, set }) => (
            <label key={label} className="flex items-center gap-2 cursor-pointer">
              <div
                onClick={() => set(!value)}
                className={`w-10 h-5 rounded-full relative transition-colors duration-300 ${value ? "bg-primary" : "bg-muted"}`}
              >
                <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-primary-foreground transition-transform duration-300 ${value ? "translate-x-5" : "translate-x-0.5"}`} />
              </div>
              <span className="text-sm text-foreground">{label}</span>
            </label>
          ))}
        </div>

        {/* Forge button */}
        <button
          ref={btnRef}
          onClick={handleForge}
          disabled={!prompt.trim() || isProcessing}
          className="relative w-full py-4 rounded-xl font-display font-bold text-lg text-primary-foreground overflow-hidden transition-all duration-300 hover:scale-[1.02] active:scale-[0.98] disabled:opacity-50 disabled:hover:scale-100 shimmer-btn"
          style={{
            background: "linear-gradient(135deg, hsl(263 84% 58%), hsl(340 100% 59%), hsl(263 84% 58%))",
            backgroundSize: "200% 200%",
            animation: isProcessing ? "pipeline-flow 2s linear infinite" : undefined,
          }}
        >
          <span className="relative z-10 flex items-center justify-center gap-2">
            {isProcessing ? (
              <>
                <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24" fill="none">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" strokeDasharray="60 30" />
                </svg>
                FORGING...
              </>
            ) : (
              <>
                <Zap className="w-5 h-5" />
                FORGE YOUR PROMPT
              </>
            )}
          </span>
        </button>
      </div>
    </section>
  );
};

export default InputArena;
