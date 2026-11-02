import React from 'react';
import { CheckCircle2, Clock, AlertOctagon, HelpCircle, AlertTriangle } from 'lucide-react';
import { ClaimStatus } from '../types';

interface StatusBadgeProps {
  status: ClaimStatus;
  size?: 'sm' | 'md' | 'lg';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const configs: Record<ClaimStatus, { bg: string; text: string; border: string; icon: any; label: string }> = {
    CURRENT: {
      bg: 'bg-emerald-950/60',
      text: 'text-emerald-400',
      border: 'border-emerald-800/60',
      icon: CheckCircle2,
      label: 'CURRENT',
    },
    OUTDATED: {
      bg: 'bg-rose-950/60',
      text: 'text-rose-400',
      border: 'border-rose-800/60',
      icon: Clock,
      label: 'OUTDATED',
    },
    CONTRADICTED: {
      bg: 'bg-red-950/70',
      text: 'text-red-400',
      border: 'border-red-800/70',
      icon: AlertOctagon,
      label: 'CONTRADICTED',
    },
    TIME_SENSITIVE: {
      bg: 'bg-amber-950/60',
      text: 'text-amber-400',
      border: 'border-amber-800/60',
      icon: AlertTriangle,
      label: 'TIME SENSITIVE',
    },
    UNVERIFIED: {
      bg: 'bg-slate-900',
      text: 'text-slate-400',
      border: 'border-slate-800',
      icon: HelpCircle,
      label: 'UNVERIFIED',
    },
  };

  const current = configs[status] || configs.UNVERIFIED;
  const Icon = current.icon;

  const sizeClasses = {
    sm: 'px-2 py-0.5 text-[10px] gap-1',
    md: 'px-2.5 py-1 text-xs gap-1.5',
    lg: 'px-3 py-1.5 text-sm gap-2',
  }[size];

  return (
    <span
      className={`inline-flex items-center font-semibold rounded-md border tracking-wide uppercase ${current.bg} ${current.text} ${current.border} ${sizeClasses}`}
    >
      <Icon className={size === 'sm' ? 'h-3 w-3' : 'h-3.5 w-3.5'} />
      <span>{current.label}</span>
    </span>
  );
};

