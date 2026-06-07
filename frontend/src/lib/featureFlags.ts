export type DealixFeature = 'agents' | 'billing' | 'proofVault' | 'clientWorkspace' | 'selfServeSignup';

const defaults: Record<DealixFeature, boolean> = {
  agents: true,
  billing: false,
  proofVault: true,
  clientWorkspace: true,
  selfServeSignup: false,
};

export function isFeatureEnabled(feature: DealixFeature, overrides?: Partial<Record<DealixFeature, boolean>>) {
  return overrides?.[feature] ?? defaults[feature];
}
