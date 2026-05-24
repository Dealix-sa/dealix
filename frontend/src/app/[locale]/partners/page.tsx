import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { PartnerApplyForm } from "@/components/gtm/PartnerApplyForm";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "partners");
}

export default function PartnersPage() {
  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-4xl px-6 py-16">
        <PartnerApplyForm />
      </div>
    </PublicGtmShell>
  );
}
