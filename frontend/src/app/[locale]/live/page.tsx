import type { Metadata } from "next";
import { CompanyLive } from "@/components/live/CompanyLive";

type Props = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "Dealix تشتغل الآن — الشركة تعمل بمحرّكات حقيقية" : "Dealix, Live — The Company Running on Real Engines",
    description: isAr
      ? "أقوى الخدمات، خط أنابيب مُقيَّم، ومسودات يومية جاهزة لموافقة المؤسس. كل إجراء خارجي مسودة محكومة — لا إرسال تلقائي، لا أرقام مخترعة."
      : "Strongest services, a scored pipeline, and daily drafts ready for founder approval. Every external action is a governed draft — no auto-send, no fabricated numbers.",
    alternates: { canonical: `https://dealix.me/${locale}/live` },
  };
}

export default async function LivePage({ params }: Props) {
  const { locale } = await params;
  return <CompanyLive locale={locale} />;
}
