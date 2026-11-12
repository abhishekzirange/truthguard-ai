import React, { useEffect, useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { History, ArrowRight, Search, RefreshCw } from 'lucide-react';
import { getHistory } from '../services/api';
import { VerificationRunListItem } from '../types';

export const HistoryPage: React.FC = () => {
  const [runs, setRuns] = useState<VerificationRunListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  const loadRuns = useCallback(() => {
    setLoading(true);
    getHistory(0, 50)
      .then((data) => {
        setRuns(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    let active = true;
    getHistory(0, 50)
      .then((data) => {
        if (active) {
          setRuns(data);
          setLoading(false);
        }
      })
      .catch((err) => {
        console.error(err);
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const filtered = runs.filter(
    (r) =>
      r.original_answer.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.domain.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.id.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
            <History className="h-3.5 w-3.5 text-teal-400" />
            <span>Audit Trail</span>
          </div>
          <h1 className="text-3xl font-extrabold tracking-tight text-white">Verification History</h1>
          <p className="mt-1 text-xs text-slate-400">
            Immutable audit record of all past AI answer verifications and detected discrepancies.
          </p>
        </div>

        <button
          onClick={loadRuns}
          className="inline-flex items-center gap-2 rounded-xl border border-slate-800 bg-slate-900 px-4 py-2 text-xs font-medium text-slate-300 hover:bg-slate-800 transition-all cursor-pointer self-start sm:self-auto"
        >
          <RefreshCw className={`h-3.5 w-3.5 ${loading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* Search Bar */}
      <div className="mb-6 relative">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          placeholder="Search by answer text, domain, or run ID..."
          className="w-full rounded-xl border border-slate-800 bg-slate-950 pl-10 pr-4 py-2.5 text-xs text-slate-200 placeholder-slate-500 focus:border-indigo-500 focus:outline-none"
        />
      </div>

      {/* Runs Table */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 shadow-xl backdrop-blur-md">
        {loading ? (
          <div className="flex py-16 items-center justify-center">
            <div className="h-6 w-6 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
          </div>
        ) : filtered.length === 0 ? (
          <div className="py-16 text-center text-xs text-slate-500">
            No verification runs found. Start a verification in the Workspace.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-300">
              <thead className="border-b border-slate-800 text-slate-400 font-semibold uppercase text-[10px]">
                <tr>
                  <th className="py-3 px-3">Run ID</th>
                  <th className="py-3 px-3">Date</th>
                  <th className="py-3 px-3">Answer Preview</th>
                  <th className="py-3 px-3">Domain</th>
                  <th className="py-3 px-3">Mode</th>
                  <th className="py-3 px-3">Claims</th>
                  <th className="py-3 px-3">Outdated</th>
                  <th className="py-3 px-3">Latency</th>
                  <th className="py-3 px-3">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 font-sans">
                {filtered.map((r) => (
                  <tr key={r.id} className="hover:bg-slate-800/30 transition-colors">
                    <td className="py-3 px-3 font-mono text-slate-400 font-bold">{r.id.slice(0, 8)}</td>
                    <td className="py-3 px-3 text-slate-400 whitespace-nowrap">
                      {new Date(r.created_at).toLocaleDateString()} {new Date(r.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </td>
                    <td className="py-3 px-3 max-w-sm truncate text-slate-200">{r.original_answer}</td>
                    <td className="py-3 px-3 capitalize text-slate-400">{r.domain}</td>
                    <td className="py-3 px-3">
                      <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                        r.execution_mode === 'LIVE'
                          ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
                          : r.execution_mode === 'PARTIAL'
                          ? 'border-amber-500/30 bg-amber-500/10 text-amber-400'
                          : 'border-slate-800 bg-slate-950 text-slate-400'
                      }`}>
                        {r.execution_mode || 'OFFLINE'}
                      </span>
                    </td>
                    <td className="py-3 px-3 font-mono">{r.total_claims}</td>
                    <td className="py-3 px-3 font-mono font-bold text-rose-400">{r.outdated_count}</td>
                    <td className="py-3 px-3 font-mono text-slate-400">{r.execution_time_ms || 0} ms</td>
                    <td className="py-3 px-3">
                      <Link
                        to={`/results/${r.id}`}
                        className="inline-flex items-center gap-1 font-semibold text-indigo-400 hover:text-indigo-300"
                      >
                        <span>Inspect</span>
                        <ArrowRight className="h-3 w-3" />
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

