import { CANONICAL_OFFERS } from "@/lib/offers/canonical-offers";
import WhatsAppCTA from "@/components/WhatsAppCTA";

export const metadata = {
  title: "Dealix — الأسعار | سلم العروض الكامل",
  description:
    "أسعار Dealix الكاملة: من تشخيص مجاني إلى نظام مؤسسي مخصص. ست مراحل واضحة حسب نضج شركتك.",
};

export default function PricingPage() {
  return (
    <main dir="rtl" className="min-h-screen bg-[#06111f] px-6 py-16 text-white">
      <div className="mx-auto max-w-6xl">

        {/* Hero */}
        <p className="mb-4 inline-flex rounded-full border border-white/20 px-4 py-2 text-sm text-slate-300">
          الأسعار
        </p>
        <h1 className="max-w-4xl text-4xl font-black leading-tight md:text-6xl">
          ابدأ بإثبات القيمة. لا عقود طويلة.
        </h1>
        <p className="mt-6 max-w-3xl text-lg leading-8 text-slate-300">
          سلم عروض واحد من ست مراحل. تبدأ بتشخيص مجاني، وتتطور بالخطوة المناسبة
          لمرحلة شركتك — من حل سريع بـ 499 ريال إلى نظام مؤسسي كامل.
        </p>

        {/* Offers grid */}
        <div className="mt-12 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {CANONICAL_OFFERS.map((offer) => (
            <article
              key={offer.tier}
              className={`relative flex flex-col rounded-3xl border p-6 ${
                offer.highlight
                  ? "border-cyan-400/50 bg-cyan-400/[0.06] ring-1 ring-cyan-400/30"
                  : "border-white/10 bg-white/[0.03]"
              }`}
            >
              {offer.highlight && (
                <div className="absolute -top-3 right-6">
                  <span className="rounded-full bg-cyan-400 px-3 py-1 text-xs font-black text-[#06111f]">
                    الأكثر طلباً
                  </span>
                </div>
              )}

              <div className="flex items-start justify-between">
                <span className={`rounded-full border px-3 py-1 text-xs ${offer.badgeColor}`}>
                  {offer.badge}
                </span>
                <span className="text-sm text-slate-500">#{offer.tier}</span>
              </div>

              <h2 className="mt-4 text-2xl font-black">{offer.name}</h2>
              <p className="text-sm text-slate-400">{offer.nameAr}</p>

              <p className="mt-4 text-3xl font-black text-white">{offer.price}</p>
              <p className="mt-1 text-sm text-slate-400">{offer.duration}</p>

              <p className="mt-4 text-sm leading-7 text-slate-300">{offer.description}</p>

              <ul className="mt-4 flex-1 space-y-2">
                {offer.outputs.map((output) => (
                  <li key={output} className="flex gap-2 text-sm text-slate-300">
                    <span className="mt-0.5 text-cyan-400">✓</span>
                    <span>{output}</span>
                  </li>
                ))}
              </ul>

              <a
                href={offer.ctaHref}
                className={`mt-6 block rounded-2xl px-6 py-3 text-center text-sm font-bold transition-colors ${offer.ctaStyle}`}
              >
                {offer.cta}
              </a>
            </article>
          ))}
        </div>

        {/* Journey */}
        <section className="mt-20 rounded-3xl border border-white/10 bg-white/[0.03] p-8 md:p-12">
          <h2 className="text-3xl font-black">التسلسل الصحيح</h2>
          <p className="mt-3 text-slate-400">لا نبدأ بمشروع كبير. دائماً نبدأ بتشخيص.</p>
          <div className="mt-8 flex flex-wrap items-center gap-4 text-lg font-black">
            <a href="/ar/intake" className="text-cyan-300 hover:underline">تشخيص مجاني</a>
            <span className="text-slate-600">→</span>
            <a href="/ar/diagnostic-sprint" className="text-emerald-300 hover:underline">
              تشخيص تحولي مدفوع
            </a>
            <span className="text-slate-600">→</span>
            <a href="/ar/offers" className="text-violet-300 hover:underline">
              تشغيل شهري أو نظام مؤسسي
            </a>
          </div>
          <p className="mt-5 leading-7 text-slate-400">
            التشخيص المجاني يعطيك وضوحاً خلال 30 دقيقة. التشخيص التحولي المدفوع يحدد أين
            يتسرب الإيراد ويسلمك خارطة الحل خلال 3–7 أيام. بعد الإثبات ننتقل للتشغيل
            الشهري (2,999–4,999 ريال/شهر، مسار موسع حتى 15,000 حسب النطاق) أو نظام
            مؤسسي مخصص.
          </p>
        </section>

        {/* Governance */}
        <section className="mt-12 rounded-3xl border border-slate-700 bg-slate-900/50 p-8">
          <h2 className="text-2xl font-black">الحوكمة في كل المنتجات</h2>
          <div className="mt-5 grid gap-3 md:grid-cols-2 text-sm text-slate-300">
            {[
              "AI drafts → أنت تراجع → أنت ترسل",
              "لا auto-send في أي منتج",
              "لا scraping لبيانات خارجية",
              "لا ROI claims بدون baseline موثق",
              "لا نشر خارجي بدون موافقة صريحة",
              "لا دفع حقيقي بدون تفعيل MOYASAR_LIVE_MODE",
            ].map((rule) => (
              <div key={rule} className="flex items-center gap-3">
                <span className="text-emerald-400">✓</span>
                {rule}
              </div>
            ))}
          </div>
        </section>

        {/* CTA */}
        <section className="mt-16 text-center">
          <h2 className="text-3xl font-black">ابدأ الأسبوع القادم</h2>
          <p className="mt-3 text-slate-400">التشخيص يبدأ خلال 24 ساعة من الاتفاق.</p>
          <div className="mt-6 flex flex-wrap justify-center gap-4">
            <a
              href="/ar/intake"
              className="inline-block rounded-2xl bg-white px-10 py-4 text-xl font-black text-[#06111f] hover:bg-slate-100"
            >
              ابدأ التشخيص المجاني
            </a>
            <WhatsAppCTA
              message="السلام عليكم، أريد الاستفسار عن عروض Dealix وأسعارها."
              label="راسلنا على واتساب"
              fallbackSubject="استفسار عن الأسعار"
              className="inline-block rounded-2xl border border-emerald-400/40 px-10 py-4 text-xl font-bold text-emerald-200 hover:bg-emerald-400/10"
            />
          </div>
        </section>

      </div>
    </main>
  );
}
