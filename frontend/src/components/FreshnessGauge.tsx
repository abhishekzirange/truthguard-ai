import React from 'react';
import { CalendarOff, Sparkles, ShieldAlert } from 'lucide-react';

interface FreshnessGaugeProps {
  score: number | null;
  label?: string;
  showFormulaHint?: boolean;
}

export const FreshnessGauge: React.FC<FreshnessGaugeProps> = ({
  score,
  label = 'Freshness Score',
  showFormulaHint = false,
}) => {
  if (score === null || score === undefined) {
    return (
      <div className="flex flex-col gap-1">
        <span className="text-[11px] font-medium uppercase tracking-wider text-slate-400">{label}</span>
        <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 border border-slate-800 text-slate-400 text-xs">
          <CalendarOff className="h-3 w-3 text-slate-500" />
          <span>Insufficient Date Info</span>
        </div>
      </div>
    );
  }

  let color = 'from-emerald-500 to-teal-400';
  let textColor = 'text-emerald-400';
  if (score < 40) {
    color = 'from-rose-500 to-red-600';
    textColor = 'text-rose-400';
  } else if (score < 70) {
    color = 'from-amber-500 to-yellow-400';
    textColor = 'text-amber-400';
  }

  return (
    <div className="flex flex-col gap-1.5">
      <div className="flex items-center justify-between text-xs">
        <span className="text-[11px] font-medium uppercase tracking-wider text-slate-400">{label}</span>
        <span className={`font-mono font-bold ${textColor}`}>{score.toFixed(1)}%</span>
      </div>
      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800/80">
        <div
          className={`h-full rounded-full bg-gradient-to-r ${color} transition-all duration-500`}
          style={{ width: `${Math.min(100, Math.max(0, score))}%` }}
        />
      </div>
      {showFormulaHint && (
        <span className="text-[10px] text-slate-500 font-mono">
          Decay: 100 × 2^(-age / half_life)
        </span>
      )}
    </div>
  );
};
