export type ClaimStatus = 'CURRENT' | 'OUTDATED' | 'CONTRADICTED' | 'UNVERIFIED' | 'TIME_SENSITIVE';
export type TemporalSensitivity = 'HIGH' | 'MEDIUM' | 'LOW';

export interface EvidenceItem {
  id: string;
  claim_id: string;
  source_title: string;
  source_url: string;
  source_domain: string;
  content_snippet: string;
  published_at: string | null;
  updated_at: string | null;
  retrieved_at: string;
  relevance_score: number;
  source_reliability_score: number;
  source_type: string;
  relationship_type: 'SUPPORTING' | 'CONTRADICTING' | 'NEUTRAL';
}

export interface ClaimAssessment {
  verdict: ClaimStatus;
  freshness_score: number | null;
  evidence_quality_score: number | null;
  reasoning: string;
  suggested_correction: string | null;
  supporting_evidence_ids: string[];
  contradicting_evidence_ids: string[];
  missing_information: string[];
  assessed_at?: string;
}

export interface Claim {
  id: string;
  run_id: string;
  claim_text: string;
  subject?: string | null;
  predicate?: string | null;
  object?: string | null;
  category: string;
  temporal_sensitivity: TemporalSensitivity;
  status: ClaimStatus;
  mentioned_date?: string | null;
  mentioned_version?: string | null;
  verification_query?: string | null;
  extraction_confidence: number;
  created_at: string;
  assessment?: ClaimAssessment | null;
  evidence_count: number;
  evidence_items?: EvidenceItem[];
}

export interface VerificationSummary {
  total_claims: number;
  current_claims: number;
  outdated_claims: number;
  contradicted_claims: number;
  unverified_claims: number;
  time_sensitive_claims: number;
  overall_freshness_score: number | null;
  overall_evidence_quality_score: number | null;
}

export interface VerificationRun {
  id: string;
  original_answer: string;
  domain: string;
  freshness_policy: string;
  verification_depth: string;
  verification_status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
  execution_time_ms?: number | null;
  summary?: VerificationSummary | null;
  error_message?: string | null;
  created_at: string;
  completed_at?: string | null;
  claims: Claim[];
}

export interface VerificationRunListItem {
  id: string;
  original_answer: string;
  domain: string;
  freshness_policy: string;
  verification_status: string;
  execution_time_ms?: number | null;
  total_claims: number;
  outdated_count: number;
  current_count: number;
  contradicted_count: number;
  created_at: string;
  completed_at?: string | null;
}

export interface CategoryMetric {
  category: string;
  count: number;
  outdated_count: number;
}

export interface ProblematicClaim {
  claim_text: string;
  status: string;
  category: string;
  verdict_reasoning: string;
  suggested_correction?: string | null;
  created_at: string;
}

export interface MetricsResponse {
  total_runs: number;
  total_claims: number;
  outdated_claims: number;
  contradicted_claims: number;
  unverified_claims: number;
  current_claims: number;
  average_latency_ms: number;
  average_freshness_score: number | null;
  total_input_tokens: number;
  total_output_tokens: number;
  estimated_total_cost_usd: number;
  status_distribution: {
    current: number;
    outdated: number;
    contradicted: number;
    unverified: number;
    time_sensitive: number;
  };
  category_distribution: CategoryMetric[];
  recent_problematic_claims: ProblematicClaim[];
}

export interface IntegrationStatus {
  configured: boolean;
  reachable: boolean;
  latency_ms?: number | null;
  message: string;
  details?: Record<string, any>;
}

export interface IntegrationsReport {
  tavily: IntegrationStatus;
  bifrost: IntegrationStatus;
  database: IntegrationStatus;
}

