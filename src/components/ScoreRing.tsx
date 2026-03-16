import { useEffect, useState, useRef } from "react";

interface ScoreRingProps {
  score: number;
  maxScore?: number;
  label: string;
  animate?: boolean;
}

const ScoreRing = ({ score, maxScore = 10, label, animate = true }: ScoreRingProps) => {
  const [currentScore, setCurrentScore] = useState(0);
  const [drawn, setDrawn] = useState(false);
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!animate) {
      setCurrentScore(score);
      setDrawn(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !drawn) {
          setDrawn(true);
          let start = 0;
          const step = score / 30;
          const interval = setInterval(() => {
            start += step;
            if (start >= score) {
              setCurrentScore(score);
              clearInterval(interval);
            } else {
              setCurrentScore(Math.round(start * 10) / 10);
            }
          }, 30);
        }
      },
      { threshold: 0.5 }
    );

    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [score, animate, drawn]);

  const radius = 40;
  const circumference = 2 * Math.PI * radius;
  const percent = currentScore / maxScore;
  const offset = circumference * (1 - percent);

  const getColor = () => {
    if (percent >= 0.8) return "hsl(157 100% 50%)";
    if (percent >= 0.5) return "hsl(51 100% 50%)";
    return "hsl(340 100% 59%)";
  };

  return (
    <div ref={ref} className="glass-card p-5 flex flex-col items-center gap-3 hover:scale-105 transition-transform duration-300">
      <div className="relative">
        <svg width="100" height="100" viewBox="0 0 100 100">
          <circle
            cx="50" cy="50" r={radius}
            fill="none"
            stroke="hsl(245 30% 17%)"
            strokeWidth="6"
          />
          <circle
            cx="50" cy="50" r={radius}
            fill="none"
            stroke={getColor()}
            strokeWidth="6"
            strokeLinecap="round"
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            transform="rotate(-90 50 50)"
            style={{
              transition: "stroke-dashoffset 1s ease-out",
              filter: `drop-shadow(0 0 6px ${getColor()})`,
            }}
          />
        </svg>
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="font-display text-xl font-bold" style={{ color: getColor() }}>
            {currentScore.toFixed(1)}
          </span>
        </div>
      </div>
      <span className="text-xs font-mono text-muted-foreground uppercase tracking-wider">
        {label}
      </span>
    </div>
  );
};

export default ScoreRing;
