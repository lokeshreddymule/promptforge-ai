const AuroraBackground = () => {
  return (
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <div
        className="absolute w-[800px] h-[800px] rounded-full opacity-30 blur-[120px]"
        style={{
          background: "radial-gradient(circle, hsl(263 84% 58% / 0.6), transparent 70%)",
          top: "-20%",
          left: "-10%",
          animation: "aurora 20s ease-in-out infinite",
        }}
      />
      <div
        className="absolute w-[600px] h-[600px] rounded-full opacity-20 blur-[100px]"
        style={{
          background: "radial-gradient(circle, hsl(186 100% 50% / 0.5), transparent 70%)",
          top: "-10%",
          right: "-5%",
          animation: "aurora 25s ease-in-out infinite reverse",
        }}
      />
      <div
        className="absolute w-[500px] h-[500px] rounded-full opacity-15 blur-[80px]"
        style={{
          background: "radial-gradient(circle, hsl(340 100% 59% / 0.4), transparent 70%)",
          bottom: "10%",
          left: "30%",
          animation: "aurora 30s ease-in-out infinite",
        }}
      />
    </div>
  );
};

export default AuroraBackground;
