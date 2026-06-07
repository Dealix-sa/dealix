import type { Metadata } from "next";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import { ContactForm } from "@/components/gtm/ContactForm";

type PageProps = {
  params: Promise<{ locale: string }>;
  searchParams: Promise<{ email?: string; plan?: string }>;
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "تواصل مع Dealix — ابدأ تشخيصك" : "Contact Dealix — Start your diagnostic",
    description: isAr
      ? "تحدّث مع فريق Dealix. تشخيص محكوم بالأدلة، حلول AI مخصّصة، امتثال PDPL و ZATCA. لا تسويق بارد آلي."
      : "Talk to the Dealix team. Evidence-governed diagnostics, custom AI solutions, PDPL & ZATCA compliance. No cold outreach.",
    alternates: { canonical: `https://dealix.me/${locale}/contact` },
  };
}

export default async function ContactPage({ params, searchParams }: PageProps) {
  const { locale } = await params;
  const sp = await searchParams;
  const isAr = locale === "ar";

  return (
    <PublicGtmShell compactNav>
      <div className="mx-auto max-w-3xl px-6 py-12" dir={isAr ? "rtl" : "ltr"}>
        <header className="text-center mb-10">
          <h1 className="text-3xl md:text-4xl font-bold">
            {isAr ? "لنبدأ المحادثة" : "Let's start the conversation"}
          </h1>
          <p className="mt-3 text-muted-foreground max-w-xl mx-auto">
            {isAr
              ? "أخبرنا عن شركتك وما تريد تحقيقه. نراجع كل طلب يدوياً ونرد خلال ساعات العمل."
              : "Tell us about your company and what you want to achieve. Every request is reviewed manually and answered within business hours."}
          </p>
        </header>

        <ContactForm defaultEmail={sp.email ?? ""} defaultPlan={sp.plan ?? ""} />
      </div>
    </PublicGtmShell>
  );
}
