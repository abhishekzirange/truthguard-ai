import {
  VerificationRun,
  VerificationRunListItem,
  MetricsResponse,
  IntegrationsReport,
  Claim,
  EvidenceItem
} from '../types';

const API_BASE = '/api/v1';

export async function submitVerification(params: {
  answer_text: string;
  domain: string;
  verification_depth: string;
  freshness_policy: string;
}): Promise<VerificationRun> {
  const response = await fetch(`${API_BASE}/verify`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Verification request failed (${response.status})`);
  }
  return response.json();
}

export async function getVerificationRun(id: string): Promise<VerificationRun> {
  const response = await fetch(`${API_BASE}/verify/${id}`);
  if (!response.ok) {
    throw new Error(`Failed to load verification run ${id}`);
  }
  return response.json();
}

export async function getRunClaims(id: string): Promise<Claim[]> {
  const response = await fetch(`${API_BASE}/verify/${id}/claims`);
  if (!response.ok) {
    throw new Error(`Failed to load claims for run ${id}`);
  }
  return response.json();
}

export async function getClaimEvidence(claimId: string): Promise<EvidenceItem[]> {
  const response = await fetch(`${API_BASE}/claims/${claimId}/evidence`);
  if (!response.ok) {
    throw new Error(`Failed to load evidence for claim ${claimId}`);
  }
  return response.json();
}

export async function getHistory(skip = 0, limit = 50): Promise<VerificationRunListItem[]> {
  const response = await fetch(`${API_BASE}/history?skip=${skip}&limit=${limit}`);
  if (!response.ok) {
    throw new Error('Failed to load verification history');
  }
  return response.json();
}

export async function getMetrics(): Promise<MetricsResponse> {
  const response = await fetch(`${API_BASE}/metrics`);
  if (!response.ok) {
    throw new Error('Failed to load system metrics');
  }
  return response.json();
}

export async function getIntegrationsStatus(): Promise<IntegrationsReport> {
  const response = await fetch(`${API_BASE}/integrations/status`);
  if (!response.ok) {
    throw new Error('Failed to check integrations status');
  }
  return response.json();
}

