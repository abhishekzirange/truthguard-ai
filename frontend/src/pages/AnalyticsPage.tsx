import React, { useEffect, useState } from 'react';
import {
  BarChart3,
  TrendingUp,
  Clock,
  Layers,
  DollarSign,
  PieChart as PieIcon,
  ShieldCheck
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
  Legend
} from 'recharts';
import { getMetrics } from '../services/api';
import { MetricsResponse } from '../types';

const STATUS_COLORS: Record<string, string> = {
  Current: '#10b981',
  Outdated: '#f43f5e',
  Contradicted: '#ef4444',
  Unverified: '#64748b',
  'Time Sensitive': '#f59e0b',
};

export const AnalyticsPage: React.FC = () => {
  const [metrics, setMetrics] = useState<MetricsResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMetrics()
      .then((data) => {
        setMetrics(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
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

  const categoryData = metrics?.category_distribution || [];
  const statusPieData = metrics
    ? [
        { name: 'Current', value: metrics.status_distribution.current, color: STATUS_COLORS.Current },
        { name: 'Outdated', value: metrics.status_distribution.outdated, color: STATUS_COLORS.Outdated },
        { name: 'Contradicted', value: metrics.status_distribution.contradicted, color: STATUS_COLORS.Contradicted },
        { name: 'Unverified', value: metrics.status_distribution.unverified, color: STATUS_COLORS.Unverified },
        { name: 'Time Sensitive', value: metrics.status_distribution.time_sensitive, color: STATUS_COLORS['Time Sensitive'] },
      ].filter((d) => d.value > 0)
    : [];

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
          <BarChart3 className="h-3.5 w-3.5 text-teal-400" />
          <span>Reliability Intelligence</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white">TruthGuard Verification Analytics</h1>
        <p className="mt-1 text-xs text-slate-400">
          Aggregated epistemic telemetry, model consumption metrics, and category vulnerability rates.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">Total Claims Audited</span>
          <span className="text-3xl font-extrabold font-mono text-white">{metrics?.total_claims || 0}</span>
          <span className="text-[11px] text-slate-500 block mt-2">Parsed into Subject-Predicate triples</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">Average Freshness</span>
          <span className="text-3xl font-extrabold font-mono text-emerald-400">
            {metrics?.average_freshness_score !== null ? `${metrics?.average_freshness_score}%` : 'N/A'}
          </span>
          <span className="text-[11px] text-slate-500 block mt-2">Exponential decay curve</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">Total Gateway Tokens</span>
          <span className="text-3xl font-extrabold font-mono text-blue-400">
            {((metrics?.total_input_tokens || 0) + (metrics?.total_output_tokens || 0)).toLocaleString()}
          </span>
          <span className="text-[11px] text-slate-500 block mt-2">Bifrost LLM gateway traffic</span>
        </div>

        <div className="rounded-xl border border-slate-800 bg-slate-900/40 p-5">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400 block mb-1">Estimated Cost</span>
          <span className="text-3xl font-extrabold font-mono text-slate-200">
            ${(metrics?.estimated_total_cost_usd || 0).toFixed(4)}
          </span>
          <span className="text-[11px] text-slate-500 block mt-2">Per-token billing tracking</span>
        </div>
      </div>

      {/* Recharts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Category Breakdown BarChart */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-sm font-semibold text-white mb-2">Claims by Category & Outdated Volume</h2>
          <p className="text-xs text-slate-400 mb-6">Which categories suffer from the highest rate of stale answers.</p>

          <div className="h-72 w-full">
            {categoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={categoryData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                  <XAxis dataKey="category" tick={{ fill: '#94a3b8', fontSize: 11 }} angle={-25} textAnchor="end" />
                  <YAxis tick={{ fill: '#94a3b8', fontSize: 11 }} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#1e293b', borderRadius: '8px', fontSize: '12px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                  <Bar dataKey="count" name="Total Claims" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="outdated_count" name="Outdated Claims" fill="#f43f5e" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center text-xs text-slate-500">
                No category data available yet.
              </div>
            )}
          </div>
        </div>

        {/* Status Distribution PieChart */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
          <h2 className="text-sm font-semibold text-white mb-2">Claim Status Ratio</h2>
          <p className="text-xs text-slate-400 mb-6">Epistemic breakdown across verified information.</p>

          <div className="h-72 w-full">
            {statusPieData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={statusPieData}
                    dataKey="value"
                    nameKey="name"
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={95}
                    paddingAngle={4}
                  >
                    {statusPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{ backgroundColor: '#090d16', borderColor: '#1e293b', borderRadius: '8px', fontSize: '12px' }}
                  />
                  <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex h-full items-center justify-center text-xs text-slate-500">
                No status ratio data yet.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
