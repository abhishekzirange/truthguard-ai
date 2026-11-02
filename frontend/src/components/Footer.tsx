import React from 'react';
import { ShieldCheck, ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-slate-900 bg-[#05080f] py-8 text-xs text-slate-500">
      <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-4 px-4 sm:flex-row sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <ShieldCheck className="h-4 w-4 text-teal-400" />
          <span className="font-semibold text-slate-300">TruthGuard AI</span>
          <span>— Autonomous Stale-Answer Detection Platform</span>
        </div>
        <div className="flex items-center gap-6">
          <span className="text-slate-400">Powered by Tavily & Bifrost AI Gateway</span>
          <span className="font-mono text-slate-600">v1.0.0</span>
        </div>
      </div>
    </footer>
  );
};
