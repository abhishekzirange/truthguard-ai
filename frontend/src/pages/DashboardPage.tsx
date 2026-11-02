import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  Activity,
  Layers,
  Clock,
  AlertOctagon,
  CheckCircle2,
  HelpCircle,
  TrendingUp,
  DollarSign,
  ArrowRight,
  ExternalLink,
  ShieldCheck,
  AlertTriangle
} from 'lucide-react';
import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts';
import { getMetrics, getHistory } from '../services/api';
import { MetricsResponse, VerificationRunListItem } from '../types';
import { StatusBadge } from '../components/StatusBadge';

const STATUS_COLORS: Record<string, string> = {
  CURRENT: '#10b981',
  OUTDATED: '#f43f5e',
  CONTRADICTED: '#ef4444',
  UNVERIFIED: '#64748b',
  TIME_SENSITIVE: '#f59e0b',
};

export const DashboardPage: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [recentRuns, setRecentRuns] = useState<VerificationRunListItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getMetrics(), getHistory(0, 5)])
      .then(([metricsData, historyData]) => {
        setMetrics(metricsData);
        setRecentRuns(historyData);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Failed to load dashboard metrics', err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      </div>
    );
  }

  const pieData = metrics
    ? [
        { name: 'Current', value: metrics.status_distribution.current, color: STATUS_COLORS.CURRENT },
        { name: 'Outdated', value: metrics.status_distribution.outdated, color: STATUS_COLORS.OUTDATED },
        { name: 'Contradicted', value: metrics.status_distribution.contradicted, color: STATUS_COLORS.CONTRADICTED },
        { name: 'Unverified', value: metrics.status_distribution.unverified, color: STATUS_COLORS.UNVERIFIED },
        { name: 'Time Sensitive', value: metrics.status_distribution.time_sensitive, color: STATUS_COLORS.TIME_SENSITIVE },
      ].filter((d) => d.value > 0)
    : [];

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Dashboard Top Header */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
            <Activity className="h-3.5 w-3.5 text-teal-400" />
            <span>Platform Telemetry</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">TruthGuard Intelligence Dashboard</h1>
          <p className="mt-1 text-xs text-slate-400">
            Real-time analytics on AI answer freshness, detected hallucinations, and verification performance.
          </p>
        </div>

        <Link
          to="/workspace"
          className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 px-5 py-2.5 text-xs font-semibold text-white shadow-md shadow-indigo-600/20 hover:scale-105 transition-all"
        >
          <span>Run Verification</span>
          <ArrowRight className="h-3.5 w-3.5" />
        </Link>
      </div>

      {/* Primary KPI Metrics Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-xs text-slate-400 block mb-1">Total Verification Runs</span>
          <span className="text-3xl font-extrabold font-mono text-white">{metrics?.total_runs || 0}</span>
          <span className="text-[11px] text-slate-500 block mt-2">Persisted in PostgreSQL</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-xs text-slate-400 block mb-1">Total Claims Audited</span>
          <span className="text-3xl font-extrabold font-mono text-indigo-300">{metrics?.total_claims || 0}</span>
          <span className="text-[11px] text-slate-500 block mt-2">Decomposed atomic triples</span>
        </div>

        <div className="rounded-xl border border-rose-900/40 bg-rose-950/20 p-5">
          <span className="text-xs text-rose-400 block mb-1">Outdated Claims Detected</span>
          <span className="text-3xl font-extrabold font-mono text-rose-300">{metrics?.outdated_claims || 0}</span>
          <span className="text-[11px] text-rose-400/70 block mt-2">Superseded knowledge</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-xs text-slate-400 block mb-1">Average Latency</span>
          <span className="text-3xl font-extrabold font-mono text-teal-300">{metrics?.average_latency_ms || 0} ms</span>
          <span className="text-[11px] text-slate-500 block mt-2">End-to-end execution</span>
        </div>
      </div>

      {/* Secondary Metrics Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 flex items-center justify-between">
          <div>
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Average Freshness</span>
            <span className="text-xl font-bold font-mono text-emerald-400">
              {metrics?.average_freshness_score !== null ? `${metrics?.average_freshness_score}%` : 'N/A'}
            </span>
          </div>
          <TrendingUp className="h-6 w-6 text-emerald-500/40" />
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 flex items-center justify-between">
          <div>
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Total Model Tokens</span>
            <span className="text-xl font-bold font-mono text-blue-400">
              {((metrics?.total_input_tokens || 0) + (metrics?.total_output_tokens || 0)).toLocaleString()}
            </span>
          </div>
          <Layers className="h-6 w-6 text-blue-500/40" />
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-950/60 p-4 flex items-center justify-between">
          <div>
            <span className="text-[11px] text-slate-400 uppercase tracking-wider block">Estimated Cost</span>
            <span className="text-xl font-bold font-mono text-slate-200">
              ${(metrics?.estimated_total_cost_usd || 0).toFixed(4)}
            </span>
          </div>
          <DollarSign className="h-6 w-6 text-slate-500" />
        </div>
      </div>

      {/* Grid: Status Distribution Chart & Recent Problem Claims */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        {/* Claim Status Chart */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <h2 className="text-sm font-semibold text-white mb-4">Claim Verdict Distribution</h2>
          <div className="h-56 w-full flex items-center justify-center">
            {pieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#1e293b', borderRadius: '8px', fontSize: '12px' }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-xs text-slate-500">No verification data yet.</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-2 text-xs pt-3 border-t border-slate-800/80">
            {pieData.map((d) => (
              <div key={d.name} className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full" style={{ backgroundColor: d.color }} />
                <span className="text-slate-400">{d.name}:</span>
                <span className="font-mono font-bold text-slate-200">{d.value}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Problem Claims (Outdated / Contradicted) */}
        <div className="lg:col-span-2 rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-sm font-semibold text-white flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-rose-400" />
              <span>Flagged Stale & Contradicted Claims</span>
            </h2>
            <span className="text-xs text-slate-500">Live Audit Feed</span>
          </div>

          <div className="space-y-3 flex-1 overflow-y-auto max-h-80">
            {metrics?.recent_problematic_claims && metrics.recent_problematic_claims.length > 0 ? (
              metrics.recent_problematic_claims.map((claim, idx) => (
                <div key={idx} className="rounded-xl bg-slate-950/70 border border-slate-800/80 p-3.5 text-xs space-y-2">
                  <div className="flex items-center justify-between">
                    <StatusBadge status={claim.status as any} size="sm" />
                    <span className="text-[10px] font-mono text-slate-500 uppercase">{claim.category}</span>
                  </div>
                  <p className="text-slate-200 font-medium leading-relaxed">"{claim.claim_text}"</p>
                  <p className="text-slate-400 text-[11px] leading-relaxed">{claim.verdict_reasoning}</p>
                  {claim.suggested_correction && (
                    <div className="rounded bg-emerald-950/30 border border-emerald-900/40 p-2 text-emerald-300 font-mono text-[11px]">
                      Correction: {claim.suggested_correction}
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="flex flex-1 items-center justify-center py-12 text-xs text-slate-500">
                No problematic claims recorded yet.
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Recent Verification Runs Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-semibold text-white">Recent Verification Runs</h2>
          <Link to="/history" className="text-xs text-indigo-400 hover:text-indigo-300 flex items-center gap-1">
            <span>View All History</span>
            <ArrowRight className="h-3 w-3" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="border-b border-slate-800 text-slate-400 font-medium">
              <tr>
                <th className="py-2.5 px-3">Run ID</th>
                <th className="py-2.5 px-3">Answer Preview</th>
                <th className="py-2.5 px-3">Domain</th>
                <th className="py-2.5 px-3">Claims</th>
                <th className="py-2.5 px-3">Outdated</th>
                <th className="py-2.5 px-3">Status</th>
                <th className="py-2.5 px-3">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {recentRuns.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3 px-3 font-mono text-slate-400">{r.id.slice(0, 8)}</td>
                  <td className="py-3 px-3 max-w-xs truncate text-slate-200">{r.original_answer}</td>
                  <td className="py-3 px-3 capitalize text-slate-400">{r.domain}</td>
                  <td className="py-3 px-3 font-mono">{r.total_claims}</td>
                  <td className="py-3 px-3 font-mono text-rose-400 font-bold">{r.outdated_count}</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded bg-emerald-950/60 text-emerald-400 border border-emerald-800/60 text-[10px] font-semibold">
                      {r.verification_status}
                    </span>
                  </td>
                  <td className="py-3 px-3">
                    <Link
                      to={`/results/${r.id}`}
                      className="text-indigo-400 hover:text-indigo-300 font-semibold"
                    >
                      View Report
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
