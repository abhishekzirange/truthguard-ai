import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ShieldCheck,
  Clock,
  Sparkles,
  ArrowLeft,
  Filter,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  ExternalLink,
  Layers,
  ArrowRight,
  TrendingUp,
  FileText,
  Radio,
  Wifi,
  WifiOff,
  Database,
  Cpu
} from 'lucide-react';
import { getVerificationRun } from '../services/api';
import { VerificationRun, Claim, ClaimStatus } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { FreshnessGauge } from '../components/FreshnessGauge';

export const ResultsPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [run, setRun] = useState<VerificationRun | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('ALL');

  useEffect(() => {
    if (id) {
      getVerificationRun(id)
        .then((data) => {
          setRun(data);
          setLoading(false);
        })
        .catch((err) => {
          setError(err.message || 'Failed to load report.');
          setLoading(false);
        });
    }
  }, [id]);

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
          <p className="text-xs font-mono text-slate-400">Loading Verification Report...</p>
        </div>
      </div>
    );
  }

  if (error || !run) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-16 text-center">
        <AlertTriangle className="mx-auto h-12 w-12 text-rose-400 mb-4" />
        <h2 className="text-xl font-bold text-white mb-2">Report Not Found</h2>
        <p className="text-sm text-slate-400 mb-6">{error || 'This verification report does not exist.'}</p>
        <Link
          to="/workspace"
          className="inline-flex items-center gap-2 rounded-lg bg-indigo-600 px-5 py-2.5 text-xs font-semibold text-white"
        >
          <ArrowLeft className="h-4 w-4" />
          <span>Back to Workspace</span>
        </Link>
      </div>
    );
  }

  const summary = run.summary || {
    total_claims: run.claims.length,
    current_claims: run.claims.filter((c) => c.status === 'CURRENT').length,
    outdated_claims: run.claims.filter((c) => c.status === 'OUTDATED').length,
    contradicted_claims: run.claims.filter((c) => c.status === 'CONTRADICTED').length,
    unverified_claims: run.claims.filter((c) => c.status === 'UNVERIFIED').length,
    time_sensitive_claims: run.claims.filter((c) => c.status === 'TIME_SENSITIVE').length,
    overall_freshness_score: null,
    overall_evidence_quality_score: null,
  };

  const filteredClaims = run.claims.filter((claim) => {
    if (statusFilter === 'ALL') return true;
    return claim.status === statusFilter;
  });

  const execMode = run.execution_mode || 'OFFLINE';

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Top Bar Navigation */}
      <div className="mb-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <Link
          to="/workspace"
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>New Verification</span>
        </Link>

        <div className="flex items-center gap-3">
          <Link
            to={`/evidence/${run.id}`}
            className="inline-flex items-center gap-2 rounded-lg border border-indigo-500/30 bg-indigo-500/10 px-4 py-2 text-xs font-semibold text-indigo-300 hover:bg-indigo-500/20 transition-all shadow-sm"
          >
            <Layers className="h-3.5 w-3.5 text-teal-400" />
            <span>Open Evidence Explorer (3-Column Matrix)</span>
            <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>
      </div>

      {/* Execution Mode Banner */}
      <div className={`mb-6 rounded-2xl border p-4.5 backdrop-blur-md flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${
        execMode === 'LIVE'
          ? 'border-emerald-500/30 bg-emerald-950/20 text-emerald-300'
          : execMode === 'PARTIAL'
          ? 'border-amber-500/30 bg-amber-950/20 text-amber-300'
          : 'border-slate-800 bg-slate-900/60 text-slate-300'
      }`}>
        <div className="flex items-center gap-3">
          <div className={`h-9 w-9 rounded-xl flex items-center justify-center shrink-0 ${
            execMode === 'LIVE' ? 'bg-emerald-500/20 text-emerald-400' : execMode === 'PARTIAL' ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-400'
          }`}>
            {execMode === 'LIVE' ? <Wifi className="h-5 w-5" /> : execMode === 'PARTIAL' ? <Radio className="h-5 w-5" /> : <Database className="h-5 w-5" />}
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider">
                Execution Mode: {execMode} VERIFICATION
              </span>
              <span className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${
                execMode === 'LIVE'
                  ? 'border-emerald-500/40 bg-emerald-500/10 text-emerald-300'
                  : execMode === 'PARTIAL'
                  ? 'border-amber-500/40 bg-amber-500/10 text-amber-300'
                  : 'border-slate-700 bg-slate-800 text-slate-400'
              }`}>
                {execMode === 'LIVE' ? (run.claims[0]?.assessment?.provenance || 'LIVE_TAVILY') : execMode === 'PARTIAL' ? 'PARTIAL_EXTERNAL' : 'OFFLINE_DETERMINISTIC'}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              {execMode === 'LIVE'
                ? 'Ground-truth verified via real-time Tavily search retrieval and authoritative web consensus.'
                : execMode === 'PARTIAL'
                ? 'Executed with partial external API connectivity. Missing components fell back safely to deterministic rules.'
                : 'Executed in offline deterministic mode with PEP 440 SemVer parsing, pattern consensus, and verified corpus.'}
            </p>
          </div>
        </div>

        {run.integration_status && (
          <div className="text-right text-[11px] font-mono text-slate-400 shrink-0 border-t sm:border-t-0 sm:border-l border-slate-800 pt-2 sm:pt-0 sm:pl-4">
            <div>Tavily: <span className={run.integration_status?.tavily?.status === 'HEALTHY' ? 'text-emerald-400' : 'text-slate-500'}>{run.integration_status?.tavily?.status || 'N/A'}</span></div>
            <div>Bifrost: <span className={run.integration_status?.bifrost?.status === 'HEALTHY' ? 'text-emerald-400' : 'text-slate-500'}>{run.integration_status?.bifrost?.status || 'N/A'}</span></div>
          </div>
        )}
      </div>

      {/* Verification Executive Summary Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/50 p-6 shadow-xl backdrop-blur-md mb-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 border-b border-slate-800 pb-6 mb-6">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-mono uppercase px-2.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700">
                Run #{run.id.slice(0, 8)}
              </span>
              <span className="text-xs text-slate-400">
                Domain: <strong className="text-slate-200 capitalize">{run.domain}</strong>
              </span>
              <span className="text-xs text-slate-400">
                Policy: <strong className="text-slate-200 capitalize">{run.freshness_policy}</strong>
              </span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight">Verification Audit Summary</h1>
          </div>

          <div className="flex items-center gap-6">
            <div className="text-right">
              <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">Execution Latency</span>
              <span className="font-mono text-base font-bold text-slate-200">{run.execution_time_ms || 0} ms</span>
            </div>
            <div className="w-36">
              <FreshnessGauge
                score={summary.overall_freshness_score}
                label="Avg Freshness"
                showFormulaHint
              />
            </div>
          </div>
        </div>

        {/* Claim Count Metric Badges */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div className="rounded-xl bg-slate-950/60 border border-slate-800 p-3.5">
            <span className="text-xs text-slate-400 block mb-1">Total Claims</span>
            <span className="text-2xl font-bold font-mono text-white">{summary.total_claims}</span>
          </div>

          <div className="rounded-xl bg-rose-950/20 border border-rose-900/40 p-3.5">
            <span className="text-xs text-rose-400 block mb-1">Outdated</span>
            <span className="text-2xl font-bold font-mono text-rose-300">{summary.outdated_claims}</span>
          </div>

          <div className="rounded-xl bg-red-950/20 border border-red-900/40 p-3.5">
            <span className="text-xs text-red-400 block mb-1">Contradicted</span>
            <span className="text-2xl font-bold font-mono text-red-300">{summary.contradicted_claims}</span>
          </div>

          <div className="rounded-xl bg-emerald-950/20 border border-emerald-900/40 p-3.5">
            <span className="text-xs text-emerald-400 block mb-1">Current</span>
            <span className="text-2xl font-bold font-mono text-emerald-300">{summary.current_claims}</span>
          </div>

          <div className="rounded-xl bg-slate-950/60 border border-slate-800 p-3.5">
            <span className="text-xs text-slate-400 block mb-1">Unverified</span>
            <span className="text-2xl font-bold font-mono text-slate-300">{summary.unverified_claims}</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1">
          {['ALL', 'OUTDATED', 'CONTRADICTED', 'CURRENT', 'UNVERIFIED'].map((status) => (
            <button
              key={status}
              onClick={() => setStatusFilter(status)}
              className={`rounded-lg px-3 py-1.5 text-xs font-semibold transition-all cursor-pointer ${
                statusFilter === status
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-900 text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              {status}
            </button>
          ))}
        </div>

        <span className="text-xs text-slate-500 font-mono">
          Showing {filteredClaims.length} of {run.claims.length} claims
        </span>
      </div>

      {/* Claim Cards List */}
      <div className="space-y-4">
        {filteredClaims.map((claim: Claim, idx: number) => {
          const assessment = claim.assessment;
          const provenance = assessment?.provenance || 'OFFLINE_DETERMINISTIC';
          return (
            <div
              key={claim.id}
              className={`rounded-xl border p-5 transition-all ${
                claim.status === 'OUTDATED'
                  ? 'border-rose-800/40 bg-rose-950/10'
                  : claim.status === 'CONTRADICTED'
                  ? 'border-red-800/40 bg-red-950/10'
                  : claim.status === 'CURRENT'
                  ? 'border-emerald-800/30 bg-emerald-950/10'
                  : 'border-slate-800 bg-slate-900/40'
              }`}
            >
              {/* Claim Card Header */}
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800/60 pb-3 mb-3">
                <div className="flex items-center flex-wrap gap-2">
                  <span className="font-mono text-xs text-slate-500 font-bold">#{idx + 1}</span>
                  <StatusBadge status={claim.status} size="sm" />
                  <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-slate-950 text-slate-400 border border-slate-800">
                    {claim.category}
                  </span>
                  <span className={`text-[10px] font-semibold px-2 py-0.5 rounded ${
                    claim.temporal_sensitivity === 'HIGH' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' : 'text-slate-500'
                  }`}>
                    {claim.temporal_sensitivity} SENSITIVITY
                  </span>
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded border ${
                    provenance.startsWith('LIVE')
                      ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400'
                      : provenance.startsWith('PARTIAL')
                      ? 'border-amber-500/30 bg-amber-500/10 text-amber-400'
                      : 'border-slate-800 bg-slate-950 text-slate-400'
                  }`}>
                    {provenance}
                  </span>
                </div>

                <div className="flex items-center gap-4 text-xs">
                  {assessment?.freshness_score !== undefined && assessment?.freshness_score !== null && (
                    <span className="text-slate-400">
                      Freshness: <strong className="text-slate-200 font-mono">{assessment.freshness_score}%</strong>
                    </span>
                  )}
                  {assessment?.evidence_quality_score !== undefined && assessment?.evidence_quality_score !== null && (
                    <span className="text-slate-400">
                      Evidence Quality: <strong className="text-slate-200 font-mono">{assessment.evidence_quality_score}%</strong>
                    </span>
                  )}
                  <Link
                    to={`/evidence/${run.id}`}
                    className="inline-flex items-center gap-1 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
                  >
                    <span>{claim.evidence_count || claim.evidence_items?.length || 2} sources</span>
                    <ExternalLink className="h-3 w-3" />
                  </Link>
                </div>
              </div>

              {/* Claim Text */}
              <div className="mb-3">
                <p className="text-sm font-medium text-slate-100 leading-relaxed">
                  "{claim.claim_text}"
                </p>
              </div>

              {/* Reasoning & Correction Box */}
              {assessment && (
                <div className="rounded-lg bg-slate-950/70 border border-slate-800/80 p-3.5 space-y-2 text-xs">
                  <div>
                    <span className="font-semibold text-slate-400 uppercase tracking-wider text-[10px] block mb-1">
                      TruthGuard Assessment Reasoning:
                    </span>
                    <p className="text-slate-300 leading-relaxed">{assessment.reasoning}</p>
                  </div>

                  {assessment.suggested_correction && (
                    <div className="rounded bg-emerald-950/30 border border-emerald-900/50 p-2.5 mt-2">
                      <span className="font-semibold text-emerald-400 uppercase tracking-wider text-[10px] block mb-1">
                        Suggested Evidence-Backed Correction:
                      </span>
                      <p className="text-emerald-200 font-medium">{assessment.suggested_correction}</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
