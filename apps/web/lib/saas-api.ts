export type SaasHealth = {
  status: string;
  saas_foundation: boolean;
  live_outbound: boolean;
  live_billing: boolean;
};

export async function getSaasHealth(): Promise<SaasHealth> {
  return {
    status: "ok",
    saas_foundation: true,
    live_outbound: false,
    live_billing: false,
  };
}
