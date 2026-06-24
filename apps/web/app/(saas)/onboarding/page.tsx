import { OnboardingChecklist } from "@/components/saas/onboarding-checklist";

export default function SaasOnboardingPage() {
  return (
    <main className="mx-auto max-w-4xl p-8">
      <h1 className="text-3xl font-bold">Dealix SaaS Onboarding</h1>
      <p className="mt-3 text-muted-foreground">Founder-led beta setup. No live outbound or billing capture.</p>
      <div className="mt-8"><OnboardingChecklist /></div>
    </main>
  );
}
