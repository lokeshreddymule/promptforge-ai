import ScoreRing from "./ScoreRing";
import { Copy, Check } from "lucide-react";
import { useState, useEffect, useRef } from "react";

export interface ForgeResult {
  detectedType: string;
  problems: string[];
  improvements: string[];
  originalPrompt: string;
  optimizedPrompt: string;
  scores: { clarity: number; specificity: number; context: number; structure: number };
  originalScores?: { clarity: number; specificity: number; context: number; structure: number };
  improvement: number;
  criticVerdict: "APPROVED" | "NEEDS_REVISION";
  criticFeedback: { label: string; text: string }[];
  originalResponse: string;
  optimizedResponse: string;
  originalScore?: number;
  optimizedScore?: number;
}

const CopyButton = ({ text }: { text: string }) => {
  const [copied, setCopied] = useState(false);
  return (
    <button onClick={() => { navigator.clipboard.writeText(text); setCopied(true); setTimeout(() => setCopied(false), 2000); }}
      className="p-1.5 rounded-md hover:bg-muted/50 transition-colors text-muted-foreground hover:text-foreground">
      {copied ? <Check className="w-4 h-4 text-neon-green" /> : <Copy className="w-4 h-4" />}
    </button>
  );
};

const AnimatedCounter = ({ value }: { value: number }) => {
  const [current, setCurrent] = useState(0);
  const ref = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        let start = 0;
        const step = value / 40;
        const interval = setInterval(() => {
          start += step;
          if (start >= value) { setCurrent(value); clearInterval(interval); }
          else setCurrent(Math.round(start));
        }, 25);
        observer.disconnect();
      }
    }, { threshold: 0.5 });
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [value]);
  return (
    <div ref={ref} className="font-display text-6xl sm:text-7xl font-800 text-neon-green neon-text-cyan">
      +{current}%
    </div>
  );
};

const TypeWriter = ({ text, speed = 8 }: { text: string; speed?: number }) => {
  const [displayed, setDisplayed] = useState("");
  useEffect(() => {
    setDisplayed("");
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) { setDisplayed(text.slice(0, i + 1)); i++; }
      else clearInterval(interval);
    }, speed);
    return () => clearInterval(interval);
  }, [text]);
  return <span>{displayed}<span className="animate-pulse">|</span></span>;
};

const ResultsBento = ({ result }: { result: ForgeResult }) => {
  const origTotal = result.originalScore || 3.5;
  const optTotal = result.optimizedScore || 8.0;

  return (
    <section className="relative z-20 max-w-5xl mx-auto px-4 py-16 space-y-6">
      <h2 className="font-display text-3xl sm:text-4xl font-bold mb-10 text-center gradient-text-primary">Results</h2>

      {/* Improvement banner */}
      <div className="glass-card p-8 text-center neon-glow-cyan">
        <AnimatedCounter value={result.improvement} />
        <p className="text-muted-foreground text-sm mt-2 font-mono">Overall Improvement</p>
        <div className="flex items-center justify-center gap-4 mt-4 text-sm font-mono">
          <span className="text-destructive">{origTotal}/10 Original</span>
          <span className="text-muted-foreground">→</span>
          <span className="text-neon-green">{optTotal}/10 Optimized</span>
        </div>
        {/* Score progress bar */}
        <div className="mt-4 max-w-md mx-auto">
          <div className="h-2 bg-muted rounded-full overflow-hidden">
            <div className="h-full rounded-full transition-all duration-1000"
              style={{ width: `${(optTotal / 10) * 100}%`, background: "linear-gradient(to right, hsl(263 84% 58%), hsl(157 100% 50%))" }} />
          </div>
        </div>
      </div>

      {/* Row 1 */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="glass-card p-5">
          <p className="text-xs font-mono text-muted-foreground mb-2">DETECTED TYPE</p>
          <span className="inline-block px-3 py-1 rounded-full text-sm font-mono bg-primary/20 text-primary border border-primary/30">
            {result.detectedType}
          </span>
        </div>
        <div className="glass-card p-5">
          <p className="text-xs font-mono text-muted-foreground mb-3">PROBLEMS FOUND</p>
          <div className="flex flex-wrap gap-1.5">
            {result.problems.map((p, i) => (
              <span key={i} className="px-2 py-0.5 rounded text-xs font-mono bg-destructive/15 text-destructive border border-destructive/20">✗ {p}</span>
            ))}
          </div>
        </div>
        <div className="glass-card p-5">
          <p className="text-xs font-mono text-muted-foreground mb-3">IMPROVEMENTS</p>
          <div className="flex flex-wrap gap-1.5">
            {result.improvements.map((p, i) => (
              <span key={i} className="px-2 py-0.5 rounded text-xs font-mono bg-neon-green/10 text-neon-green border border-neon-green/20">✓ {p}</span>
            ))}
          </div>
        </div>
      </div>

      {/* Row 2 — prompts */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass-card p-5 border-l-2 border-l-destructive">
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-mono text-destructive">ORIGINAL PROMPT</p>
            <CopyButton text={result.originalPrompt} />
          </div>
          <p className="font-mono text-sm text-muted-foreground leading-relaxed">{result.originalPrompt}</p>
        </div>
        <div className="glass-card p-5 border-l-2 border-l-neon-green" style={{ boxShadow: "0 0 20px hsl(157 100% 50% / 0.05)" }}>
          <div className="flex items-center justify-between mb-3">
            <p className="text-xs font-mono text-neon-green">OPTIMIZED PROMPT</p>
            <CopyButton text={result.optimizedPrompt} />
          </div>
          <p className="font-mono text-sm text-foreground leading-relaxed whitespace-pre-wrap">{result.optimizedPrompt}</p>
        </div>
      </div>

      {/* Row 3 — Score rings */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <ScoreRing score={result.scores.clarity} label="Clarity" />
        <ScoreRing score={result.scores.specificity} label="Specificity" />
        <ScoreRing score={result.scores.context} label="Context" />
        <ScoreRing score={result.scores.structure} label="Structure" />
      </div>

      {/* Row 4 — Critic */}
      <div className="glass-card p-6">
        <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full text-sm font-mono mb-5 ${
          result.criticVerdict === "APPROVED"
            ? "bg-neon-green/10 text-neon-green border border-neon-green/20"
            : "bg-destructive/10 text-destructive border border-destructive/20"
        }`}>
          {result.criticVerdict === "APPROVED" ? "✓ APPROVED" : "✗ NEEDS REVISION"}
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {result.criticFeedback.map((fb, i) => (
            <div key={i} className="p-3 rounded-lg bg-muted/20 border border-border">
              <p className="text-xs font-mono text-primary mb-1">{fb.label}</p>
              <p className="text-sm text-muted-foreground">{fb.text}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Row 5 — Responses */}
      <h3 className="font-display text-2xl font-bold text-center gradient-text-primary pt-8">Response Arena</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="glass-card p-5 relative scanlines border-l-2 border-l-destructive">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-destructive">BEFORE — Original Prompt Response</span>
            <CopyButton text={result.originalResponse} />
          </div>
          <p className="font-mono text-xs text-muted-foreground leading-relaxed whitespace-pre-wrap max-h-64 overflow-y-auto">
            {result.originalResponse}
          </p>
        </div>
        <div className="glass-card p-5 relative scanlines border-l-2 border-l-neon-green">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono text-neon-green">AFTER — Optimized Prompt Response</span>
            <CopyButton text={result.optimizedResponse} />
          </div>
          <p className="font-mono text-xs text-foreground leading-relaxed whitespace-pre-wrap max-h-64 overflow-y-auto">
            <TypeWriter text={result.optimizedResponse} />
          </p>
        </div>
      </div>
    </section>
  );
};

export default ResultsBento;
