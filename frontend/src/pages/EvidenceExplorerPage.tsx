import React, { useCallback, useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft,
  ExternalLink,
  Calendar,
  Layers,
  Globe
} from 'lucide-react';
import { getVerificationRun, getClaimEvidence } from '../services/api';
import { VerificationRun, Claim, EvidenceItem } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { FreshnessGauge } from '../components/FreshnessGauge';

export const EvidenceExplorerPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [run, setRun] = useState<VerificationRun | null>(null);
  const [selectedClaimIndex, setSelectedClaimIndex] = useState(0);
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingEvidence, setLoadingEvidence] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadEvidenceForClaim = useCallback(async (claimId: string) => {
    setLoadingEvidence(true);
    try {
      const items = await getClaimEvidence(claimId);
      setEvidenceList(items);
    } catch {
      setEvidenceList([]);
    } finally {
      setLoadingEvidence(false);
    }
  }, []);

  useEffect(() => {
    if (id) {
      getVerificationRun(id)
        .then((data) => {
          setRun(data);
          setLoading(false);
          if (data.claims.length > 0) {
            loadEvidenceForClaim(data.claims[0].id);
          }
        })
        .catch((err) => {
          setError(err.message || 'Failed to load report');
          setLoading(false);
        });
    }
  }, [id, loadEvidenceForClaim]);

  const handleSelectClaim = (idx: number) => {
    if (!run) return;
    setSelectedClaimIndex(idx);
    loadEvidenceForClaim(run.claims[idx].id);
  };

  if (loading) {
    return (
      <div className="flex min-h-[60vh] items-center justify-center">
        <div className="h-8 w-8 animate-spin rounded-full border-2 border-indigo-500 border-t-transparent" />
      </div>
    );
  }

  if (error || !run || run.claims.length === 0) {
    return (
      <div className="mx-auto max-w-4xl px-4 py-16 text-center">
        <p className="text-slate-400">No verification evidence available.</p>
        <Link to="/workspace" className="mt-4 inline-block text-xs text-indigo-400">Back to Workspace</Link>
      </div>
    );
  }

  const currentClaim: Claim = run.claims[selectedClaimIndex];
  const assessment = currentClaim.assessment;

  return (
    <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
      {/* Navigation Top */}
      <div className="mb-6 flex items-center justify-between">
        <Link
          to={`/results/${run.id}`}
          className="inline-flex items-center gap-2 text-xs font-medium text-slate-400 hover:text-white transition-colors"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Back to Verification Summary</span>
        </Link>
        <span className="text-xs font-mono text-slate-400">
          Run #{run.id.slice(0, 8)} • Evidence Matrix
        </span>
      </div>

      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Layers className="h-6 w-6 text-teal-400" />
          <span>Evidence Explorer (3-Column Matrix)</span>
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Compare the original AI assertion against retrieved live primary sources and TruthGuard's mathematical scoring.
        </p>
      </div>

      {/* Claim Selector Horizontal Tabs */}
      <div className="mb-6 flex items-center gap-2 overflow-x-auto pb-2">
        {run.claims.map((c, idx) => (
          <button
            key={c.id}
            onClick={() => handleSelectClaim(idx)}
            className={`flex items-center gap-2 px-3.5 py-2 rounded-xl text-xs font-medium transition-all whitespace-nowrap cursor-pointer ${
              selectedClaimIndex === idx
                ? 'bg-indigo-600 text-white shadow-md'
                : 'bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <span className="font-mono font-bold">#{idx + 1}</span>
            <span className="max-w-[150px] truncate">{c.claim_text}</span>
            <StatusBadge status={c.status} size="sm" />
          </button>
        ))}
      </div>

      {/* 3-Column Matrix Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Column 1: ORIGINAL CLAIM */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="border-b border-slate-800 pb-3 mb-4">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-indigo-400 block mb-1">Column 1</span>
            <h2 className="text-base font-bold text-white">Original AI Claim</h2>
          </div>

          <div className="rounded-xl bg-slate-950 p-4 border border-slate-800/80 mb-4">
            <p className="text-sm font-medium text-slate-100 leading-relaxed">
              "{currentClaim.claim_text}"
            </p>
          </div>

          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between border-b border-slate-800/40 pb-2">
              <span className="text-slate-400">Category:</span>
              <span className="font-mono font-semibold text-slate-200">{currentClaim.category}</span>
            </div>
            <div className="flex justify-between border-b border-slate-800/40 pb-2">
              <span className="text-slate-400">Temporal Sensitivity:</span>
              <span className={`font-semibold ${
                currentClaim.temporal_sensitivity === 'HIGH' ? 'text-amber-400' : 'text-slate-300'
              }`}>{currentClaim.temporal_sensitivity}</span>
            </div>
            {currentClaim.mentioned_version && (
              <div className="flex justify-between border-b border-slate-800/40 pb-2">
                <span className="text-slate-400">Claimed Version:</span>
                <span className="font-mono text-indigo-300 font-bold">{currentClaim.mentioned_version}</span>
              </div>
            )}
            <div className="pt-2">
              <span className="text-slate-400 block mb-1">Generated Query:</span>
              <span className="font-mono text-[11px] text-slate-300 bg-slate-950 p-2 rounded block border border-slate-800">
                {currentClaim.verification_query || 'Default search query'}
              </span>
            </div>
          </div>
        </div>

        {/* Column 2: CURRENT EVIDENCE */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="border-b border-slate-800 pb-3 mb-4 flex items-center justify-between">
            <div>
              <span className="text-[11px] font-semibold uppercase tracking-wider text-teal-400 block mb-1">Column 2</span>
              <h2 className="text-base font-bold text-white">Retrieved Evidence</h2>
            </div>
            <span className="text-xs font-mono text-slate-400">
              {evidenceList.length} sources found
            </span>
          </div>

          {loadingEvidence ? (
            <div className="flex flex-1 items-center justify-center py-12">
              <div className="h-6 w-6 animate-spin rounded-full border-2 border-teal-400 border-t-transparent" />
            </div>
          ) : evidenceList.length === 0 ? (
            <div className="flex flex-1 items-center justify-center py-12 text-center text-xs text-slate-500">
              No direct web sources retrieved.
            </div>
          ) : (
            <div className="space-y-3.5 flex-1 overflow-y-auto max-h-[500px] pr-1">
              {evidenceList.map((ev, i) => (
                <div key={ev.id || i} className="rounded-xl bg-slate-950/80 border border-slate-800 p-3.5 text-xs space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    {ev.source_url && (ev.source_url.startsWith('http://') || ev.source_url.startsWith('https://')) ? (
                      <a
                        href={ev.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-semibold text-slate-200 hover:text-teal-400 transition-colors flex items-center gap-1 leading-snug"
                      >
                        <span>{ev.source_title}</span>
                        <ExternalLink className="h-3 w-3 shrink-0 text-slate-500" />
                      </a>
                    ) : (
                      <span className="font-semibold text-slate-400 flex items-center gap-1 leading-snug">
                        <span>{ev.source_title}</span>
                      </span>
                    )}
                  </div>

                  <p className="text-slate-300 text-[11px] leading-relaxed bg-slate-900/60 p-2 rounded border border-slate-800/60">
                    "{ev.content_snippet}"
                  </p>

                  <div className="flex flex-wrap items-center justify-between gap-2 text-[10px] text-slate-400 pt-1 border-t border-slate-900">
                    <span className="flex items-center gap-1 font-mono text-slate-300">
                      <Globe className="h-3 w-3 text-slate-500" />
                      {ev.source_domain}
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="h-3 w-3 text-slate-500" />
                      {ev.published_at ? new Date(ev.published_at).toLocaleDateString() : 'Date Unknown'}
                    </span>
                    <span className="font-semibold px-1.5 py-0.5 rounded bg-slate-800 text-teal-300">
                      Reliability: {Math.round(ev.source_reliability_score * 100)}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Column 3: TRUTHGUARD ASSESSMENT */}
        <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-5 flex flex-col">
          <div className="border-b border-slate-800 pb-3 mb-4">
            <span className="text-[11px] font-semibold uppercase tracking-wider text-rose-400 block mb-1">Column 3</span>
            <h2 className="text-base font-bold text-white">TruthGuard Assessment</h2>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-xs text-slate-400">Verdict:</span>
              <StatusBadge status={currentClaim.status} size="md" />
            </div>

            <div className="rounded-xl bg-slate-950 p-3.5 border border-slate-800">
              <FreshnessGauge
                score={assessment?.freshness_score ?? null}
                label="Freshness Score"
                showFormulaHint
              />
            </div>

            <div className="rounded-xl bg-slate-950 p-3.5 border border-slate-800 text-xs">
              <div className="flex justify-between items-center mb-1">
                <span className="text-slate-400 uppercase font-semibold text-[10px]">Evidence Quality Score</span>
                <span className="font-mono font-bold text-teal-400">{assessment?.evidence_quality_score ?? 50.0}%</span>
              </div>
              <p className="text-[10px] text-slate-500 font-mono">
                Formula: 100 × (0.45·S + 0.35·R + 0.20·F/100)
              </p>
            </div>

            <div className="rounded-xl bg-slate-950 p-3.5 border border-slate-800 text-xs">
              <span className="text-slate-400 uppercase font-semibold text-[10px] block mb-1">Assessment Reasoning:</span>
              <p className="text-slate-200 leading-relaxed">
                {assessment?.reasoning || 'Claim validated against primary sources.'}
              </p>
            </div>

            {assessment?.suggested_correction && (
              <div className="rounded-xl bg-emerald-950/30 border border-emerald-900/50 p-3.5 text-xs">
                <span className="text-emerald-400 uppercase font-semibold text-[10px] block mb-1">Suggested Correction:</span>
                <p className="text-emerald-200 font-medium">
                  {assessment.suggested_correction}
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

