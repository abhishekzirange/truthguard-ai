import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ShieldCheck, Activity, History, BarChart3, Settings, Sparkles } from 'lucide-react';
import { getIntegrationsStatus } from '../services/api';

export const Navbar: React.FC = () => {
  const location = useLocation();
  const [tavilyOnline, setTavilyOnline] = useState<boolean | null>(null);

  useEffect(() => {
    let active = true;
    getIntegrationsStatus()
      .then((res) => {
        if (active) {
          setTavilyOnline(Boolean(res.tavily?.configured && res.tavily?.reachable));
        }
      })
      .catch(() => {
        if (active) setTavilyOnline(false);
      });
    return () => {
      active = false;
    };
  }, [location.pathname]);

  const navLinks = [
    { to: '/workspace', label: 'Verify', icon: Sparkles },
    { to: '/dashboard', label: 'Dashboard', icon: Activity },
    { to: '/history', label: 'History', icon: History },
    { to: '/analytics', label: 'Analytics', icon: BarChart3 },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/80 bg-[#070b14]/90 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-8">
          <Link to="/" className="flex items-center gap-3 group">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-indigo-600 via-blue-600 to-teal-400 p-0.5 shadow-lg shadow-indigo-500/20 group-hover:scale-105 transition-transform">
              <div className="flex h-full w-full items-center justify-center rounded-[10px] bg-[#090d16]">
                <ShieldCheck className="h-5 w-5 text-teal-400" />
              </div>
            </div>
            <div>
              <span className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
                TruthGuard <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">AI</span>
              </span>
              <p className="text-[10px] text-slate-400 tracking-wider uppercase font-medium">Don't Trust. Verify.</p>
            </div>
          </Link>

          <nav className="hidden md:flex items-center gap-1" aria-label="Main navigation">
            {navLinks.map((link) => {
              const Icon = link.icon;
              const isActive = location.pathname === link.to;
              return (
                <Link
                  key={link.to}
                  to={link.to}
                  className={`flex items-center gap-2 px-3.5 py-2 text-sm font-medium rounded-lg transition-all ${
                    isActive
                      ? 'bg-slate-800/80 text-white shadow-sm border border-slate-700/60'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
                  }`}
                >
                  <Icon className={`h-4 w-4 ${isActive ? 'text-teal-400' : 'text-slate-400'}`} />
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center gap-3">
          <Link
            to="/settings"
            title="View Tavily Search integration status"
            className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs text-slate-300 hover:border-slate-700 transition-colors"
          >
            <span
              className={`flex h-2 w-2 rounded-full ${
                tavilyOnline === true ? 'bg-emerald-400' : tavilyOnline === false ? 'bg-amber-400' : 'bg-slate-500'
              }`}
            />
            <span className="font-mono text-[11px] text-slate-400">
              {tavilyOnline === true ? 'Tavily: Live' : tavilyOnline === false ? 'Tavily: Offline' : 'Tavily: Checking'}
            </span>
          </Link>

          <Link
            to="/workspace"
            className="flex items-center gap-2 rounded-lg bg-gradient-to-r from-indigo-500 to-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-md shadow-indigo-600/20 hover:from-indigo-600 hover:to-blue-700 transition-all hover:shadow-indigo-600/30"
          >
            <Sparkles className="h-3.5 w-3.5" />
            <span>Verify Answer</span>
          </Link>
        </div>
      </div>
    </header>
  );
};
