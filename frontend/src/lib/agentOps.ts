export type AgentRisk = 'low' | 'medium' | 'high';
export type AgentStatus = 'queued' | 'running' | 'needs_approval' | 'done' | 'rejected';
export function requiresApproval(risk: AgentRisk, externalAction: boolean) {
  return externalAction || risk === 'high' || risk === 'medium';
}
