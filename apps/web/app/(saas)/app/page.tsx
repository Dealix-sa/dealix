import { PlanBadge } from "@/components/saas/plan-badge";
import { TenantSwitcher } from "@/components/saas/tenant-switcher";

export default function SaasAppPage() {
  return (
    <main className="mx-auto max-w-5xl p-8">
      <div className="flex items-center justify-between"><h1 className="text-3xl font-bold">Dealix OS</h1><PlanBadge /></div>
      <div className="mt-6"><TenantSwitcher /></div>
      <p className="mt-6">Revenue Command Room, Company Brain, Client Delivery, and Proof Packs.</p>
    </main>
  );
}
