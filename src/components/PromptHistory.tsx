import { useState } from "react";
import { Trash2, ChevronDown, ChevronUp, Copy, Check } from "lucide-react";
import { HistoryEntry } from "@/pages/Index";

interface Props {
  history: HistoryEntry[];
  onClear: () => void;
}

const PromptHistory = ({ history, onClear }: Props) => {
  const [expanded, setExpanded] = useState<number | null>(null);
  const [copied, setCopied] = useState<number | null>(null);

  const handleCopy = (id: number, text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  return (
    <section className="relative z-20 max-w-5xl mx-auto px-4 py-16">
      <div className="flex items-center justify-between mb-10">
        <h2 className="font-display text-3xl sm:text-4xl font-bold gradient-text-primary">
          Prompt History
        </h2>
        <button
          onClick={onClear}
          className="flex items-center gap-2 px-4 py-2 rounded-lg border border-destructive/30 text-destructive text-sm hover:bg-destructive/10 transition-colors font-mono"
        >
          <Trash2 className="w-4 h-4" />
          Clear All
        </button>
      </div>

      <div className="space-y-3">
        {history.map((entry) => (
          <div key={entry.id} className="glass-card overflow-hidden">
            {/* Header row */}
            <div
              className="flex items-center justify-between p-4 cursor-pointer hover:bg-muted/20 transition-colors"
              onClick={() => setExpanded(expanded === entry.id ? null : entry.id)}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="px-2 py-0.5 rounded-full text-xs font-mono bg-primary/15 text-primary border border-primary/20 shrink-0">
                  {entry.promptType}
                </span>
                <span className="font-mono text-sm text-muted-foreground truncate">
                  {entry.originalPrompt.slice(0, 60)}...
                </span>
              </div>
              <div className="flex items-center gap-3 shrink-0 ml-2">
                <div className="hidden sm:flex items-center gap-2 text-xs font-mono">
                  <span className="text-destructive">{entry.originalScore}/10</span>
                  <span className="text-muted-foreground">→</span>
                  <span className="text-neon-green">{entry.optimizedScore}/10</span>
                  <span className="text-neon-green font-bold">+{entry.improvement}%</span>
                </div>
                <span className="text-xs text-muted-foreground hidden md:block">{entry.timestamp}</span>
                {expanded === entry.id ? (
                  <ChevronUp className="w-4 h-4 text-muted-foreground" />
                ) : (
                  <ChevronDown className="w-4 h-4 text-muted-foreground" />
                )}
              </div>
            </div>

            {/* Expanded content */}
            {expanded === entry.id && (
              <div className="border-t border-border p-4 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-xs font-mono text-destructive">ORIGINAL</p>
                    <button onClick={() => handleCopy(entry.id * 10, entry.originalPrompt)} className="p-1 hover:text-foreground text-muted-foreground transition-colors">
                      {copied === entry.id * 10 ? <Check className="w-3 h-3 text-neon-green" /> : <Copy className="w-3 h-3" />}
                    </button>
                  </div>
                  <p className="font-mono text-xs text-muted-foreground leading-relaxed bg-background/40 rounded-lg p-3 border border-border">
                    {entry.originalPrompt}
                  </p>
                </div>
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-xs font-mono text-neon-green">OPTIMIZED</p>
                    <button onClick={() => handleCopy(entry.id * 10 + 1, entry.optimizedPrompt)} className="p-1 hover:text-foreground text-muted-foreground transition-colors">
                      {copied === entry.id * 10 + 1 ? <Check className="w-3 h-3 text-neon-green" /> : <Copy className="w-3 h-3" />}
                    </button>
                  </div>
                  <p className="font-mono text-xs text-foreground leading-relaxed bg-background/40 rounded-lg p-3 border border-neon-green/20">
                    {entry.optimizedPrompt}
                  </p>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  );
};

export default PromptHistory;
