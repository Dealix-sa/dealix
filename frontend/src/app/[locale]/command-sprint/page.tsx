import type { Metadata } from "next";
import { CommandSprintLanding } from "@/components/gtm/launch/CommandSprintLanding";
import { buildFunnelMetadata } from "@/lib/gtmMetadata";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  return buildFunnelMetadata(locale, "command-sprint");
}

export default function CommandSprintPage() {
  return <CommandSprintLanding />;
}
