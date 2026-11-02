import React, { useEffect, useState } from 'react';
import {
  Settings,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  RefreshCw,
  Search,
  Cpu,
  Database,
  Sliders,
  ExternalLink,
  Lock
} from 'lucide-react';
import { getIntegrationsStatus } from '../services/api';
import { IntegrationsReport } from '../types';

export const SettingsPage: React.FC = () => {
  const [report, setReport] = useState<IntegrationsReport | null>(null);
  const [loading, setLoading] = useState(true);
  const [testing, setTesting] = useState(false);

  const checkStatus = () => {
    setTesting(true);
    getIntegrationsStatus()
      .then((data) => {
        setReport(data);
        setLoading(false);
        setTesting(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
        setTesting(false);
      });
  };

  useEffect(() => {
    checkStatus();
  }, []);

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
            <Settings className="h-3.5 w-3.5 text-teal-400" />
            <span>Infrastructure & Diagnostics</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">System Settings & Gateway Status</h1>
          <p className="mt-1 text-xs text-slate-400">
            Audit backend connections, AI gateway configurations, and mathematical freshness decay policies.
          </p>
        </div>

        <button
          onClick={checkStatus}
          disabled={testing}
          className="inline-flex items-center gap-2 rounded-xl bg-slate-900 border border-slate-800 px-4 py-2.5 text-xs font-semibold text-slate-200 hover:bg-slate-800 transition-all cursor-pointer disabled:opacity-50 self-start sm:self-auto"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${testing ? 'animate-spin text-teal-400' : ''}`} />
          <span>Test Integrations</span>
        </button>
      </div>

      {/* Security Banner */}
      <div className="mb-8 rounded-xl bg-slate-900/60 border border-slate-800 p-4 flex items-center gap-3 text-xs text-slate-400">
        <Lock className="h-4 w-4 text-teal-400 shrink-0" />
        <span>
          <strong>Enterprise Credential Isolation:</strong> API keys for Tavily and Bifrost Gateway are securely managed by the FastAPI server environment. Keys are never transmitted to client browsers.
        </span>
      </div>

      {/* Integrations Health Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">
        {/* Tavily Search Status */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400">
                <Search className="h-4 w-4" />
              </div>
              <h2 className="text-sm font-bold text-white">Tavily Web Search</h2>
            </div>
            {report?.tavily.configured ? (
              <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400" />
            ) : (
              <span className="flex h-2.5 w-2.5 rounded-full bg-amber-400" />
            )}
          </div>

          <div className="space-y-2 text-xs flex-1">
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Configured:</span>
              <span className="font-semibold text-slate-200 font-mono">
                {report?.tavily.configured ? 'Configured' : 'Using Demo Knowledge Base'}
              </span>
            </div>
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Status:</span>
              <span className={`font-semibold ${report?.tavily.reachable ? 'text-emerald-400' : 'text-slate-400'}`}>
                {report?.tavily.reachable ? 'Connected' : 'Offline / Standby'}
              </span>
            </div>
            {report?.tavily.latency_ms && (
              <div className="flex justify-between border-b border-slate-800/60 pb-2">
                <span className="text-slate-400">Latency:</span>
                <span className="font-mono text-slate-200">{report.tavily.latency_ms} ms</span>
              </div>
            )}
          </div>

          <p className="mt-4 text-[11px] text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800/80">
            {report?.tavily.message || 'Checking status...'}
          </p>
        </div>

        {/* Bifrost AI Gateway Status */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
                <Cpu className="h-4 w-4" />
              </div>
              <h2 className="text-sm font-bold text-white">Bifrost Gateway</h2>
            </div>
            {report?.bifrost.configured ? (
              <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400" />
            ) : (
              <span className="flex h-2.5 w-2.5 rounded-full bg-amber-400" />
            )}
          </div>

          <div className="space-y-2 text-xs flex-1">
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Gateway Model:</span>
              <span className="font-mono text-indigo-300 font-semibold">
                {report?.bifrost.details?.model || 'gpt-4o-mini'}
              </span>
            </div>
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Inference Status:</span>
              <span className={`font-semibold ${report?.bifrost.reachable ? 'text-emerald-400' : 'text-slate-400'}`}>
                {report?.bifrost.reachable ? 'Active' : 'Deterministic Hybrid Active'}
              </span>
            </div>
          </div>

          <p className="mt-4 text-[11px] text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800/80">
            {report?.bifrost.message || 'Checking status...'}
          </p>
        </div>

        {/* Database Status */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-lg bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
                <Database className="h-4 w-4" />
              </div>
              <h2 className="text-sm font-bold text-white">Database Engine</h2>
            </div>
            <span className="flex h-2.5 w-2.5 rounded-full bg-emerald-400" />
          </div>

          <div className="space-y-2 text-xs flex-1">
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Engine:</span>
              <span className="font-mono text-slate-200 font-semibold">PostgreSQL / SQLite</span>
            </div>
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Migrations:</span>
              <span className="font-semibold text-emerald-400">Alembic Synchronized</span>
            </div>
            <div className="flex justify-between border-b border-slate-800/60 pb-2">
              <span className="text-slate-400">Connection:</span>
              <span className="font-semibold text-emerald-400">Operational</span>
            </div>
          </div>

          <p className="mt-4 text-[11px] text-slate-400 bg-slate-950 p-2.5 rounded border border-slate-800/80">
            {report?.database.message || 'Database connected'}
          </p>
        </div>
      </div>

      {/* Domain Half-Life Rules Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sliders className="h-4 w-4 text-teal-400" />
          <h2 className="text-base font-semibold text-white">Configured Category Half-Life Policies</h2>
        </div>
        <p className="text-xs text-slate-400 mb-6">
          Freshness is calculated mathematically via exponential decay: <code className="text-indigo-400">Freshness = 100 × 2^(-age / half_life)</code>.
          Different information categories decay at specialized rates.
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="border-b border-slate-800 text-slate-400 uppercase text-[10px] font-semibold">
              <tr>
                <th className="py-2.5 px-3">Information Category</th>
                <th className="py-2.5 px-3">Default Half-Life</th>
                <th className="py-2.5 px-3">Strict Policy (0.5x)</th>
                <th className="py-2.5 px-3">Relaxed Policy (1.5x)</th>
                <th className="py-2.5 px-3">Domain Rationale</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">Product Pricing</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">7 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">3.5 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">10.5 days</td>
                <td className="py-3 px-3 text-slate-400">Prices and token rates fluctuate weekly.</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">Software Versions</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">30 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">15 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">45 days</td>
                <td className="py-3 px-3 text-slate-400">Rapid release cycles and critical patches.</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">API Documentation</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">30 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">15 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">45 days</td>
                <td className="py-3 px-3 text-slate-400">Deprecations and breaking changes.</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">Regulations & Compliance</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">90 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">45 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">135 days</td>
                <td className="py-3 px-3 text-slate-400">Quarterly statutory deadlines and rule filings.</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">Company Information</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">90 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">45 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">135 days</td>
                <td className="py-3 px-3 text-slate-400">Executive changes, M&A, earnings releases.</td>
              </tr>
              <tr>
                <td className="py-3 px-3 font-semibold text-slate-100">General Technical Knowledge</td>
                <td className="py-3 px-3 font-mono text-teal-400 font-bold">365 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">182 days</td>
                <td className="py-3 px-3 font-mono text-slate-400">547 days</td>
                <td className="py-3 px-3 text-slate-400">Stable architectural paradigms and specs.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

