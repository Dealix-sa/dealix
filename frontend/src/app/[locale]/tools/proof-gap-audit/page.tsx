import type { Metadata } from "next";
import { PublicFunnelLayout } from "@/components/gtm/PublicFunnelLayout";
import { ToolRunner } from "@/components/wave3/tools/ToolRunner";
import { proofGapAudit } from "@/content/wave3/tools/proofGapAudit";
import { buildWave3Metadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildWave3Metadata(
    locale,
    "/tools/proof-gap-audit",
    "Proof Gap Audit — قِس قدرتك على الإثبات",
    "Proof Gap Audit — Measure your ability to prove",
    "قِس مدى قدرتك على إثبات ما يحدث بعد وصول الفرصة: المصدر، الدليل، الموافقة.",
    "Measure how well you can prove what happens after a lead arrives: source, evidence, approval.",
  );
}

export default function ProofGapAuditPage() {
  return (
    <PublicFunnelLayout>
      <ToolRunner tool={proofGapAudit} source="tool_proof_gap_audit" />
    </PublicFunnelLayout>
  );
}
