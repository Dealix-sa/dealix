import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { ContactForm } from "@/components/gtm/ContactForm";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "contact");
}

export default function ContactPage() {
  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-5xl px-6 py-12">
        <ContactForm />
      </div>
    </PublicGtmShell>
  );
}
