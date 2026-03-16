const Marquee = () => {
  const tips = [
    "⚡ Pro tip: Always specify output format",
    "🔥 Add role definition for 40% better results",
    "💡 Context is king in prompt engineering",
    "🚀 Specificity beats length every time",
    "🎯 Include examples for consistent outputs",
    "⚙️ Set constraints to avoid hallucinations",
    "✨ Chain-of-thought prompting boosts accuracy",
    "🧠 Multi-agent pipelines outperform single prompts",
  ];

  const content = tips.join("   •   ");

  return (
    <div className="fixed top-0 left-0 right-0 z-50 border-b border-border bg-background/80 backdrop-blur-md">
      <div className="overflow-hidden py-2">
        <div className="marquee-track">
          <span className="font-mono text-xs text-muted-foreground whitespace-nowrap px-4">
            {content}
          </span>
          <span className="font-mono text-xs text-muted-foreground whitespace-nowrap px-4">
            {content}
          </span>
        </div>
      </div>
    </div>
  );
};

export default Marquee;
