import React from 'react';
import { Link } from 'react-router-dom';
import {
  ShieldCheck,
  Search,
  Sparkles,
  Zap,
  ArrowRight,
  Clock,
  Layers,
  Database,
  CheckCircle2,
  AlertTriangle,
  GitCompare,
  FileCheck2,
  ExternalLink,
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { FreshnessGauge } from '../components/FreshnessGauge';

export const LandingPage: React.FC = () => {
  return (
    <div className="flex flex-col">
      {/* Hero Section */}
      <section className="relative overflow-hidden pt-20 pb-24 lg:pt-32 lg:pb-36">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(99,102,241,0.18),rgba(255,255,255,0))]" />
        <div className="relative mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 rounded-full border border-indigo-500/20 bg-indigo-500/10 px-4 py-1.5 text-xs font-medium text-indigo-300 mb-8 backdrop-blur-sm">
            <span className="flex h-2 w-2 rounded-full bg-teal-400 animate-pulse" />
            <span>Built for the Stale-Answer Hackathon Challenge</span>
          </div>

          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-6xl lg:text-7xl max-w-4xl mx-auto leading-[1.15]">
            Your AI Answers.{' '}
            <span className="bg-gradient-to-r from-teal-400 via-indigo-300 to-blue-500 bg-clip-text text-transparent">
              Independently Verified.
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto leading-relaxed">
            Detect outdated AI-generated information with live evidence, temporal intelligence and transparent claim-level verification.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link
              to="/workspace"
              className="flex items-center justify-center gap-2 w-full sm:w-auto rounded-xl bg-gradient-to-r from-indigo-500 via-blue-600 to-indigo-600 px-8 py-4 text-base font-semibold text-white shadow-xl shadow-indigo-600/25 hover:shadow-indigo-600/40 hover:scale-[1.02] transition-all"
            >
              <Sparkles className="h-5 w-5" />
              <span>Verify an Answer</span>
              <ArrowRight className="h-4 w-4" />
            </Link>

            <a
              href="#how-it-works"
              className="flex items-center justify-center gap-2 w-full sm:w-auto rounded-xl border border-slate-800 bg-slate-900/60 px-8 py-4 text-base font-medium text-slate-300 hover:bg-slate-800/60 hover:text-white transition-all backdrop-blur-sm"
            >
              <span>Explore How It Works</span>
            </a>
          </div>

          {/* Interactive Live Teaser Card */}
          <div className="mt-16 mx-auto max-w-3xl rounded-2xl border border-slate-800/80 bg-slate-900/60 p-6 shadow-2xl backdrop-blur-xl text-left">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3 mb-4">
              <span className="text-xs font-mono text-slate-400 flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-rose-500" />
                Live Demo Verification Audit
              </span>
              <StatusBadge status="OUTDATED" size="sm" />
            </div>

            <div className="space-y-3">
              <div className="rounded-lg bg-slate-950/70 p-3.5 border border-slate-800/50">
                <p className="text-xs font-semibold text-slate-400 mb-1 uppercase tracking-wider">AI Generated Claim:</p>
                <p className="text-sm font-medium text-slate-200">"Python 3.11 is the latest stable Python release."</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div className="rounded-lg bg-rose-950/20 border border-rose-900/40 p-3">
                  <p className="text-[11px] font-semibold text-rose-400 uppercase tracking-wider mb-1">Detected Contradiction</p>
                  <p className="text-xs text-rose-200">Python 3.12 and 3.13 have officially superseded Python 3.11 on python.org.</p>
                </div>
                <div className="rounded-lg bg-emerald-950/20 border border-emerald-900/40 p-3">
                  <p className="text-[11px] font-semibold text-emerald-400 uppercase tracking-wider mb-1">Evidence-Backed Correction</p>
                  <p className="text-xs text-emerald-200">Python 3.13 is the current stable release (Python Software Foundation).</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* The Problem Statement */}
      <section className="py-20 border-y border-slate-900 bg-[#080d1a]/50">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-indigo-400">The Problem</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Why AI Answers Go Stale
            </p>
            <p className="mt-4 text-slate-400 text-sm sm:text-base">
              LLMs answer with high confidence even when their internal knowledge cutoff is obsolete.
              Without independent live verification, users make costly decisions on outdated data.
            </p>
          </div>

          <div className="mt-14 grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-6">
              <div className="h-10 w-10 rounded-lg bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 mb-4">
                <GitCompare className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Software & API Shifts</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                APIs deprecate endpoints, dependencies update breaking syntax, and package releases outpace training sets.
              </p>
            </div>

            <div className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-6">
              <div className="h-10 w-10 rounded-lg bg-rose-500/10 border border-rose-500/20 flex items-center justify-center text-rose-400 mb-4">
                <Clock className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Fluctuating Pricing</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Cloud providers and SaaS APIs update token costs and tiers continuously. Stale pricing causes enterprise billing surprises.
              </p>
            </div>

            <div className="rounded-xl border border-slate-800/80 bg-slate-900/40 p-6">
              <div className="h-10 w-10 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 mb-4">
                <AlertTriangle className="h-5 w-5" />
              </div>
              <h3 className="text-lg font-semibold text-white mb-2">Regulatory Changes</h3>
              <p className="text-sm text-slate-400 leading-relaxed">
                Government mandates, SEC filing deadlines, and tax laws change frequently, making static models dangerous for compliance.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Workflow */}
      <section id="how-it-works" className="py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-xs font-semibold uppercase tracking-widest text-teal-400">Verification Pipeline</h2>
            <p className="mt-2 text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Transparent, Deterministic & Explainable
            </p>
            <p className="mt-4 text-slate-400 text-sm sm:text-base">
              TruthGuard AI decomposes answers into verifiable triples, retrieves live authoritative evidence,
              and calculates mathematical freshness decay.
            </p>
          </div>

          <div className="mt-16 grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="relative rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <div className="text-2xl font-bold text-slate-700 mb-3 font-mono">01</div>
              <h3 className="text-base font-semibold text-white mb-2">Claim Extraction</h3>
              <p className="text-xs text-slate-400">
                Splits AI prose into atomic Subject-Predicate-Object assertions with temporal sensitivity tags.
              </p>
            </div>

            <div className="relative rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <div className="text-2xl font-bold text-slate-700 mb-3 font-mono">02</div>
              <h3 className="text-base font-semibold text-white mb-2">Live Tavily Retrieval</h3>
              <p className="text-xs text-slate-400">
                Queries live web evidence prioritizing official registries, package indexes, and primary documentation.
              </p>
            </div>

            <div className="relative rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <div className="text-2xl font-bold text-slate-700 mb-3 font-mono">03</div>
              <h3 className="text-base font-semibold text-white mb-2">Hybrid Verification</h3>
              <p className="text-xs text-slate-400">
                Deterministic Semantic Versioning and price bounds merged with Bifrost AI Gateway reasoning.
              </p>
            </div>

            <div className="relative rounded-2xl border border-slate-800 bg-slate-900/40 p-6">
              <div className="text-2xl font-bold text-slate-700 mb-3 font-mono">04</div>
              <h3 className="text-base font-semibold text-white mb-2">Freshness Scoring</h3>
              <p className="text-xs text-slate-400">
                Computes exponential decay (100 × 2^(-age / half_life)) and epistemic evidence quality.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Footer */}
      <section className="py-20 border-t border-slate-900 bg-gradient-to-b from-[#0a0f1d] to-[#05080f] text-center">
        <div className="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-white sm:text-4xl">Ready to audit an AI answer?</h2>
          <p className="mt-4 text-slate-400 text-sm sm:text-base max-w-xl mx-auto">
            Paste any AI response and see claim-level freshness scores, detected contradictions, and primary citations in seconds.
          </p>
          <div className="mt-8">
            <Link
              to="/workspace"
              className="inline-flex items-center gap-2 rounded-xl bg-gradient-to-r from-indigo-500 to-blue-600 px-8 py-3.5 text-sm font-semibold text-white shadow-lg shadow-indigo-600/30 hover:scale-105 transition-all"
            >
              <Sparkles className="h-4 w-4" />
              <span>Launch Verification Workspace</span>
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};
