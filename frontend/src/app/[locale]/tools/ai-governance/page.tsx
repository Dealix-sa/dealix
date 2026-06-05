import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { ToolRunner } from "@/components/wave3/tools/ToolRunner";
import { aiGovernance } from "@/content/wave3/tools/aiGovernance";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/tools/ai-governance",
    "AI Governance Checklist — جاهزية الحوكمة",
    "AI Governance Checklist — Governance readiness",
    "قائمة فحص لجاهزية حوكمة الذكاء الاصطناعي: الموافقة البشرية، الخصوصية، وحدود النظام.",
    "A checklist for AI governance readiness: human approval, privacy, and system boundaries.",
  );
}

export default function AiGovernancePage() {
  return (
    <PublicFunnelLayout>
      <ToolRunner tool={aiGovernance} source="tool_ai_governance" />
    </PublicFunnelLayout>
  );
}
