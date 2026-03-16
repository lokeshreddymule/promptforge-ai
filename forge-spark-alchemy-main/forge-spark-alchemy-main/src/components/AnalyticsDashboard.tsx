import { useEffect, useRef } from "react";
import { HistoryEntry } from "@/pages/Index";

interface Props { history: HistoryEntry[]; }

const AnalyticsDashboard = ({ history }: Props) => {
  const typeCount: Record<string, number> = {};
  history.forEach((h) => { typeCount[h.promptType] = (typeCount[h.promptType] || 0) + 1; });

  const avgImprovement = history.length
    ? Math.round(history.reduce((a, b) => a + b.improvement, 0) / history.length)
    : 0;
  const bestScore = history.length ? Math.max(...history.map((h) => h.optimizedScore)) : 0;
  const avgScore = history.length
    ? (history.reduce((a, b) => a + b.optimizedScore, 0) / history.length).toFixed(1)
    : 0;

  const maxImprovement = Math.max(...history.map((h) => h.improvement), 1);

  return (
    <section className="relative z-20 max-w-5xl mx-auto px-4 py-16">
      <h2 className="font-display text-3xl sm:text-4xl font-bold mb-10 text-center gradient-text-primary">
        Analytics
      </h2>

      {/* Stat cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        {[
          { label: "Total Optimized", value: history.length, color: "text-neon-violet" },
          { label: "Avg Improvement", value: `+${avgImprovement}%`, color: "text-neon-green" },
          { label: "Best Score", value: `${bestScore}/10`, color: "text-neon-cyan" },
          { label: "Avg Score", value: `${avgScore}/10`, color: "text-neon-gold" },
        ].map(({ label, value, color }) => (
          <div key={label} className="glass-card p-5 text-center">
            <div className={`font-display text-2xl font-bold ${color}`}>{value}</div>
            <div className="text-xs font-mono text-muted-foreground mt-1 uppercase tracking-wider">{label}</div>
          </div>
        ))}
      </div>

      {/* Score trend bar chart */}
      <div className="glass-card p-6 mb-4">
        <p className="text-xs font-mono text-muted-foreground mb-4 uppercase tracking-wider">Score Trend</p>
        <div className="flex items-end gap-2 h-32">
          {history.slice(-12).reverse().map((h, i) => (
            <div key={h.id} className="flex-1 flex flex-col items-center gap-1">
              <div className="w-full flex flex-col gap-0.5 justify-end" style={{ height: "100px" }}>
                <div
                  className="w-full rounded-t bg-destructive/60 transition-all duration-700"
                  style={{ height: `${(h.originalScore / 10) * 100}px` }}
                />
                <div
                  className="w-full rounded-t bg-neon-green/70 transition-all duration-700"
                  style={{ height: `${(h.optimizedScore / 10) * 100}px`, marginTop: "2px" }}
                />
              </div>
              <span className="text-xs font-mono text-muted-foreground">#{h.id % 100}</span>
            </div>
          ))}
        </div>
        <div className="flex gap-4 mt-3">
          <span className="flex items-center gap-1 text-xs text-muted-foreground font-mono">
            <span className="w-3 h-2 rounded bg-destructive/60 inline-block" /> Original
          </span>
          <span className="flex items-center gap-1 text-xs text-muted-foreground font-mono">
            <span className="w-3 h-2 rounded bg-neon-green/70 inline-block" /> Optimized
          </span>
        </div>
      </div>

      {/* Improvement bars */}
      <div className="glass-card p-6">
        <p className="text-xs font-mono text-muted-foreground mb-4 uppercase tracking-wider">Improvement History</p>
        <div className="space-y-3">
          {history.slice(0, 8).map((h) => (
            <div key={h.id} className="space-y-1">
              <div className="flex justify-between text-xs font-mono text-muted-foreground">
                <span className="truncate max-w-[60%]">{h.originalPrompt.slice(0, 40)}...</span>
                <span className="text-neon-green">+{h.improvement}%</span>
              </div>
              <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-1000"
                  style={{
                    width: `${Math.min((h.improvement / maxImprovement) * 100, 100)}%`,
                    background: "linear-gradient(to right, hsl(263 84% 58%), hsl(157 100% 50%))",
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AnalyticsDashboard;
