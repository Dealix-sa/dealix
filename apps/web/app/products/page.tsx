import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "المنتجات — Dealix",
  description:
    "خمسة أنظمة تشغيلية للشركات B2B السعودية: غرفة القيادة، عقل الشركة، صندوق الوارد والمتابعة، الثقة والامتثال، تسليم العملاء.",
};

interface ProductSummary {
  slug: string;
  nameEn: string;
  nameAr: string;
  tagline: string;
  problem: string;
  delivery: string;
  icon: string;
}

const PRODUCTS: ProductSummary[] = [
  {
    slug: "revenue-command-room-os",
    nameEn: "Revenue Command Room OS",
    nameAr: "نظام غرفة قيادة الإيراد",
    tagline: "صفحة قرار واحدة للمؤسس، تتحدث يومياً بأرقام محققة.",
    problem: "القرارات المالية متفرقة على ملفات وواتساب بدون مصدر واحد.",
    delivery: "7 أيام للتشغيل الأول · مراجعة أسبوعية",
    icon: "⚡",
  },
  {
    slug: "company-brain-os",
    nameEn: "Company Brain OS",
    nameAr: "نظام عقل الشركة",
    tagline: "ذاكرة موحّدة للشركة: قرارات، سياسات، سياق، تاريخ.",
    problem: "المعرفة محبوسة في رؤوس الأفراد وملفات مبعثرة.",
    delivery: "7 أيام للتشغيل الأول · تحديث مستمر",
    icon: "🧠",
  },
  {
    slug: "whatsapp-inbox-followup-os",
    nameEn: "WhatsApp / Inbox Follow-up OS",
    nameAr: "نظام متابعة الواتساب والوارد",
    tagline: "طوابير متابعة منظمة من واتساب وإيميل بدون ضياع رسالة.",
    problem: "متابعات تضيع بين الإشعارات ولا أحد يملكها.",
    delivery: "5 أيام للتشغيل الأول · مراجعة يومية",
    icon: "📥",
  },
  {
    slug: "ai-trust-compliance-os",
    nameEn: "AI Trust & Compliance OS",
    nameAr: "نظام الثقة والامتثال",
    tagline: "بوابات موافقة بشرية، سجلات تدقيق، حماية بيانات PDPL.",
    problem: "كل خروج تلقائي يحمل خطر امتثال وإجراء قانوني.",
    delivery: "مدمج مع كل الأنظمة الأخرى · تدقيق ربع سنوي",
    icon: "🛡️",
  },
  {
    slug: "client-delivery-os",
    nameEn: "Client Delivery OS",
    nameAr: "نظام تسليم العملاء",
    tagline: "من اليوم صفر إلى التوسعة: خريطة عمل، أتمتة، احتفاظ، مراجعة.",
    problem: "التسليم يعتمد على مجهود فردي بدون دليل أو proof report.",
    delivery: "30 يوم للتشغيل الكامل · مراجعة شهرية",
    icon: "📦",
  },
];

export default function ProductsPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
            Products
          </p>
          <h1 className="mt-3 text-4xl font-semibold">خمسة أنظمة تشغيلية</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل نظام يحل مشكلة تشغيلية واضحة للشركات B2B السعودية. لا وعود
            إيراد مضمونة، لا شعارات فارغة — فقط أنظمة تعمل وتُقاس أسبوعياً.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2">
          {PRODUCTS.map((p) => (
            <Link
              key={p.slug}
              href={`/products/${p.slug}`}
              className="group rounded-2xl border border-white/10 bg-white/5 p-6 transition hover:border-amber-300/40 hover:bg-white/[0.07]"
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-2xl" aria-hidden>
                    {p.icon}
                  </p>
                  <h2 className="mt-3 text-lg font-semibold group-hover:text-amber-200">
                    {p.nameAr}
                  </h2>
                  <p className="text-xs text-white/60">{p.nameEn}</p>
                </div>
              </div>
              <p className="mt-4 text-sm text-white/80">{p.tagline}</p>
              <p className="mt-3 text-xs text-white/50">
                المشكلة: {p.problem}
              </p>
              <div className="mt-4 flex flex-wrap items-center gap-3 text-xs">
                <span className="rounded-full border border-amber-300/20 bg-amber-300/5 px-3 py-1 text-amber-200">
                  {p.delivery}
                </span>
              </div>
              <p className="mt-4 text-xs font-medium text-amber-300 group-hover:underline">
                عرض التفاصيل ←
              </p>
            </Link>
          ))}
        </section>

        <section className="mt-12 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">ملاحظة على النطاق والسعر</p>
          <p className="mt-2">
            كل نظام هنا يُحدد نطاقه وسعره بعد تشخيص لحجم شركتك وحدة المشكلة — لا رقم عام قبل
            ذلك. لا setup مخفي، وكل setup قابل للاسترداد خلال 14 يوم. لا auto-renewal — نذكّرك
            قبل 14 يوم من التجديد.
          </p>
        </section>

        <section className="mt-10 flex flex-wrap gap-3">
          <Link
            href="/book"
            className="rounded-full bg-amber-300 px-6 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            احجز تشخيص
          </Link>
          <Link
            href="/pricing"
            className="rounded-full border border-white/20 px-6 py-3 text-sm font-medium text-white transition hover:border-white/40"
          >
            كل التسعير
          </Link>
        </section>
      </div>
    </main>
  );
}