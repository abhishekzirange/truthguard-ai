import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Sparkles,
  Layers,
  Clock,
  ShieldCheck,
  Search,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  RotateCcw,
  Code2,
  DollarSign,
  FileText,
  Server
} from 'lucide-react';
import { submitVerification } from '../services/api';

const PRESETS = [
  {
    name: 'Software Releases (Hackathon Demo)',
    icon: Code2,
    domain: 'software',
    depth: 'standard',
    policy: 'standard',
    text: 'Python 3.11 is the latest stable Python release. FastAPI 0.100.0 is the latest version. PostgreSQL supports JSONB.',
  },
  {
    name: 'Model API Pricing',
    icon: DollarSign,
    domain: 'pricing',
    depth: 'standard',
    policy: 'strict',
    text: 'GPT-4o costs $30.00 per 1M input tokens. Legacy GPT-3.5 turbo is $0.002 per token.',
  },
  {
    name: 'Database Architecture',
    icon: Server,
    domain: 'technology',
    depth: 'quick',
    policy: 'standard',
    text: 'PostgreSQL provides JSONB data type with GIN indexing for high performance document storage and querying.',
  },
];

const DOMAINS = [
  { id: 'software', name: 'Software and APIs' },
  { id: 'technology', name: 'Technology & Architecture' },
  { id: 'pricing', name: 'Product Pricing' },
  { id: 'regulation', name: 'Government Regulations' },
  { id: 'company', name: 'Company & Business Info' },
  { id: 'general', name: 'General Knowledge' },
];

const STAGES = [
  'Processing answer & sanitizing text...',
  'Decomposing into atomic claims (Subject-Predicate-Object)...',
  'Planning targeted disambiguated search queries...',
  'Retrieving live authoritative evidence via Tavily...',
  'Running deterministic SemVer & Bifrost AI Gateway evaluation...',
  'Calculating exponential freshness decay & evidence quality...',
  'Compiling verification report & citations...',
];

export const WorkspacePage: React.FC = () => {
  const navigate = useNavigate();
  const [answerText, setAnswerText] = useState('');
  const [domain, setDomain] = useState('software');
  const [depth, setDepth] = useState('standard');
  const [freshnessPolicy, setFreshnessPolicy] = useState('standard');
  const [loading, setLoading] = useState(false);
  const [currentStageIndex, setCurrentStageIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const handleVerify = async () => {
    if (!answerText.trim() || answerText.length < 5) {
      setError('Please enter at least 5 characters of AI-generated text.');
      return;
    }

    setError(null);
    setLoading(true);
    setCurrentStageIndex(0);

    // Progressive stage update timer to inform the user of real pipeline phases
    const interval = setInterval(() => {
      setCurrentStageIndex((prev) => (prev < STAGES.length - 1 ? prev + 1 : prev));
    }, 450);

    try {
      const run = await submitVerification({
        answer_text: answerText,
        domain,
        verification_depth: depth,
        freshness_policy: freshnessPolicy,
      });
      clearInterval(interval);
      navigate(`/results/${run.id}`);
    } catch (err: any) {
      clearInterval(interval);
      setError(err.message || 'Verification failed. Please check backend connection.');
      setLoading(false);
    }
  };

  const applyPreset = (preset: typeof PRESETS[0]) => {
    setAnswerText(preset.text);
    setDomain(preset.domain);
    setDepth(preset.depth);
    setFreshnessPolicy(preset.policy);
    setError(null);
  };

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8">
        <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-3 py-1 text-xs font-semibold text-indigo-400 mb-2">
          <ShieldCheck className="h-3.5 w-3.5 text-teal-400" />
          <span>Verification Workspace</span>
        </div>
        <h1 className="text-3xl font-extrabold tracking-tight text-white sm:text-4xl">
          Audit an AI-Generated Answer
        </h1>
        <p className="mt-2 text-sm text-slate-400">
          Paste any text output from ChatGPT, Claude, or Gemini to extract claims, detect outdated facts, and review live evidence.
        </p>
      </div>

      {/* Preset Pills */}
      <div className="mb-6 flex flex-wrap items-center gap-2">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500 mr-1">Demo Presets:</span>
        {PRESETS.map((preset, idx) => {
          const Icon = preset.icon;
          return (
            <button
              key={idx}
              onClick={() => applyPreset(preset)}
              disabled={loading}
              className="inline-flex items-center gap-1.5 rounded-lg border border-slate-800 bg-slate-900/60 px-3 py-1.5 text-xs font-medium text-slate-300 hover:border-slate-700 hover:bg-slate-800 transition-all cursor-pointer disabled:opacity-50"
            >
              <Icon className="h-3.5 w-3.5 text-teal-400" />
              <span>{preset.name}</span>
            </button>
          );
        })}
      </div>

      {/* Main Workspace Card */}
      <div className="rounded-2xl border border-slate-800 bg-slate-900/40 p-6 shadow-xl backdrop-blur-md">
        {/* Answer Text Area */}
        <div className="relative mb-6">
          <div className="flex items-center justify-between mb-2">
            <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
              AI Answer Text
            </label>
            <div className="flex items-center gap-3">
              <span className="text-xs font-mono text-slate-500">
                {answerText.length} characters
              </span>
              {answerText && (
                <button
                  onClick={() => setAnswerText('')}
                  disabled={loading}
                  className="text-xs text-slate-500 hover:text-slate-300 transition-colors cursor-pointer"
                >
                  Clear
                </button>
              )}
            </div>
          </div>

          <textarea
            value={answerText}
            onChange={(e) => setAnswerText(e.target.value)}
            disabled={loading}
            placeholder="Paste AI-generated answer here... (e.g. Python 3.11 is the latest stable Python version. FastAPI 0.100.0 is the latest version. PostgreSQL supports JSONB.)"
            rows={6}
            className="w-full rounded-xl border border-slate-800 bg-slate-950/80 p-4 text-sm text-slate-100 placeholder-slate-600 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500 font-sans transition-all"
          />
        </div>

        {/* Configuration Controls */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
          {/* Domain */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Verification Domain
            </label>
            <select
              value={domain}
              onChange={(e) => setDomain(e.target.value)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
            >
              {DOMAINS.map((d) => (
                <option key={d.id} value={d.id}>
                  {d.name}
                </option>
              ))}
            </select>
          </div>

          {/* Verification Depth */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Search Depth
            </label>
            <select
              value={depth}
              onChange={(e) => setDepth(e.target.value)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
            >
              <option value="quick">Quick (Fastest, High Level)</option>
              <option value="standard">Standard (Recommended)</option>
              <option value="deep">Deep (Comprehensive Querying)</option>
            </select>
          </div>

          {/* Freshness Policy */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
              Freshness Policy
            </label>
            <select
              value={freshnessPolicy}
              onChange={(e) => setFreshnessPolicy(e.target.value)}
              disabled={loading}
              className="w-full rounded-lg border border-slate-800 bg-slate-950 px-3 py-2 text-xs text-slate-200 focus:border-indigo-500 focus:outline-none"
            >
              <option value="strict">Strict (0.5x Half-Life)</option>
              <option value="standard">Standard (Default Half-Life)</option>
              <option value="relaxed">Relaxed (1.5x Half-Life)</option>
            </select>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-6 rounded-lg bg-rose-950/40 border border-rose-800/60 p-4 text-xs text-rose-300 flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Progress Pipeline Indicator */}
        {loading && (
          <div className="mb-6 rounded-xl border border-indigo-500/20 bg-indigo-950/20 p-5">
            <div className="flex items-center justify-between mb-3">
              <span className="text-xs font-semibold text-indigo-400 uppercase tracking-wider flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-teal-400 animate-ping" />
                Pipeline Execution: Step {currentStageIndex + 1} of {STAGES.length}
              </span>
              <span className="text-xs font-mono text-slate-400">
                {Math.round(((currentStageIndex + 1) / STAGES.length) * 100)}%
              </span>
            </div>

            <p className="text-sm font-medium text-slate-200 mb-3 animate-fade-in">
              {STAGES[currentStageIndex]}
            </p>

            <div className="h-2 w-full overflow-hidden rounded-full bg-slate-900">
              <div
                className="h-full rounded-full bg-gradient-to-r from-indigo-500 via-blue-500 to-teal-400 transition-all duration-300"
                style={{ width: `${((currentStageIndex + 1) / STAGES.length) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Verify Action Button */}
        <div className="flex items-center justify-end">
          <button
            onClick={handleVerify}
            disabled={loading || !answerText.trim()}
            className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 via-blue-600 to-indigo-600 px-7 py-3 text-sm font-semibold text-white shadow-lg shadow-indigo-600/25 hover:from-indigo-600 hover:to-blue-700 transition-all disabled:opacity-50 cursor-pointer"
          >
            <Sparkles className="h-4 w-4" />
            <span>{loading ? 'Verifying Claims...' : 'Verify Answer'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

