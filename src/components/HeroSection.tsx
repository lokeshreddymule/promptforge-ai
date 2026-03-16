const HeroSection = () => {
  return (
    <section className="relative z-20 min-h-[80vh] flex flex-col items-center justify-center px-4 text-center py-20">
      {/* Aurora background */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] opacity-20"
          style={{
            background: "radial-gradient(ellipse, hsl(263 84% 58%) 0%, hsl(186 100% 50% / 0.3) 40%, transparent 70%)",
            filter: "blur(40px)",
          }}
        />
      </div>

      {/* Title */}
      <h1
        className="font-display font-bold mb-6"
        style={{
          fontSize: "clamp(3rem, 10vw, 7rem)",
          background: "linear-gradient(135deg, #818cf8, #c084fc, #38bdf8)",
          WebkitBackgroundClip: "text",
          WebkitTextFillColor: "transparent",
          backgroundClip: "text",
        }}
      >
        PromptForge AI
      </h1>

      {/* Tagline */}
      <p style={{ color: "#64748b", fontFamily: "monospace", fontSize: "1rem", maxWidth: "500px", lineHeight: "1.7" }}>
        Turn your vague ideas into precision-engineered prompts 
        and watch AI finally understand what you mean.
      </p>
    </section>
  );
};

export default HeroSection;
