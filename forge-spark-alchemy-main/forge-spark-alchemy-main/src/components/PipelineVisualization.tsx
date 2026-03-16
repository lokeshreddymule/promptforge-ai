import { useEffect, useState } from "react";
import { Search, Layers, Pencil, MessageSquare, Star, CheckCircle, Send } from "lucide-react";

interface PipelineVisualizationProps {
  activeStep: number;
}

const STEPS = [
  { icon: Send, label: "Raw Prompt", color: "neon-violet" },
  { icon: Search, label: "Analyzer", color: "neon-cyan" },
  { icon: Layers, label: "Type Detector", color: "neon-purple" },
  { icon: Pencil, label: "Rewriter", color: "neon-pink" },
  { icon: MessageSquare, label: "Critic", color: "neon-green" },
  { icon: Star, label: "Scorer", color: "neon-gold" },
  { icon: CheckCircle, label: "Optimized", color: "neon-green" },
];

const colorMap: Record<string, string> = {
  "neon-violet": "hsl(263 84% 58%)",
  "neon-cyan": "hsl(186 100% 50%)",
  "neon-purple": "hsl(262 100% 68%)",
  "neon-pink": "hsl(340 100% 59%)",
  "neon-green": "hsl(157 100% 50%)",
  "neon-gold": "hsl(51 100% 50%)",
};

const PipelineVisualization = ({ activeStep }: PipelineVisualizationProps) => {
  return (
    <section className="relative z-20 max-w-5xl mx-auto px-4 py-16">
      <h2 className="font-display text-2xl sm:text-3xl font-bold mb-10 text-center gradient-text-primary">
        Agent Pipeline
      </h2>

      <div className="relative flex items-center justify-between overflow-x-auto pb-4">
        {/* Connection line */}
        <div className="absolute top-8 left-[5%] right-[5%] h-0.5 bg-border hidden sm:block">
          <div
            className="h-full transition-all duration-700 ease-out"
            style={{
              width: `${Math.min(100, (activeStep / (STEPS.length - 1)) * 100)}%`,
              background: "linear-gradient(90deg, hsl(263 84% 58%), hsl(186 100% 50%))",
              boxShadow: "0 0 10px hsl(263 84% 58% / 0.5)",
            }}
          />
        </div>

        {STEPS.map((step, i) => {
          const Icon = step.icon;
          const isActive = i <= activeStep;
          const isCurrent = i === activeStep;
          const c = colorMap[step.color];

          return (
            <div key={i} className="relative flex flex-col items-center gap-2 z-10 min-w-[70px]">
              <div
                className={`w-14 h-14 sm:w-16 sm:h-16 rounded-xl flex items-center justify-center border transition-all duration-500 ${
                  isActive
                    ? "border-transparent"
                    : "border-border bg-card/50"
                } ${isCurrent ? "scale-110" : ""}`}
                style={
                  isActive
                    ? {
                        background: `linear-gradient(135deg, ${c}22, ${c}11)`,
                        borderColor: `${c}66`,
                        boxShadow: isCurrent ? `0 0 20px ${c}44` : `0 0 8px ${c}22`,
                      }
                    : undefined
                }
              >
                <Icon
                  className="w-5 h-5 sm:w-6 sm:h-6 transition-colors duration-500"
                  style={{ color: isActive ? c : "hsl(220 10% 40%)" }}
                />
              </div>
              <span
                className={`text-[10px] sm:text-xs font-mono transition-colors duration-500 text-center ${
                  isActive ? "text-foreground" : "text-muted-foreground"
                }`}
              >
                {step.label}
              </span>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default PipelineVisualization;
