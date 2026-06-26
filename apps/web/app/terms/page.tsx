import Link from "next/link";

export const metadata = {
  title: "الشروط والأحكام — Dealix | Terms of Service",
  description: "شروط استخدام خدمات Dealix — واضحة، بدون لغة قانونية معقدة.",
};

const TERMS = [
  {
    title: "1. الخدمات المقدمة",
    body: "تقدم Dealix خدمات استشارية وتقنية في مجال الذكاء الاصطناعي للشركات السعودية. كل عقد يحدد نطاق العمل والتسليمات بوضوح قبل البدء.",
  },
  {
    title: "2. الدفع والإلغاء",
    body: "يتم الدفع وفق الجدول المتفق عليه في كل عقد. الاشتراكات الشهرية قابلة للإلغاء بإشعار 30 يوماً. رسوم الـ Setup قابلة للاسترداد خلال 14 يوماً من البدء إذا لم تبدأ الخدمة فعلياً.",
  },
  {
    title: "3. ملكية النتائج",
    body: "كل ما يُبنى ويُسلَّم لك هو ملكك. Dealix لا تحتفظ بحقوق على مخرجاتك أو بياناتك. الأدوات العامة والـ frameworks المستخدمة تبقى ملكية Dealix.",
  },
  {
    title: "4. حدود المسؤولية",
    body: "النتائج التقديرية ليست ضمانات. Dealix تبذل قصارى جهدها لتحقيق الأهداف المتفق عليها لكنها لا تضمن نتائج تجارية محددة. القيمة التقديرية ليست قيمة مُتحقَّقة.",
  },
  {
    title: "5. السرية",
    body: "نلتزم بالحفاظ على سرية معلوماتك التجارية. لا نشاركها مع أي طرف ثالث بدون إذنك الصريح.",
  },
  {
    title: "6. الحوكمة والذكاء الاصطناعي",
    body: "جميع الإجراءات الخارجية (إرسال رسائل، اقتراح عروض، إصدار فواتير) تتطلب موافقة مسبقة من المؤسس. لا أتمتة غير محكومة.",
  },
  {
    title: "7. القانون المعمول به",
    body: "تخضع هذه الشروط لأنظمة المملكة العربية السعودية. أي نزاع يُحل بالتراضي أولاً، ثم عبر الجهات المختصة في المملكة.",
  },
];

export default function TermsPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-3xl px-6 py-20">
        <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
          الشروط والأحكام · Terms of Service
        </p>
        <h1 className="mt-4 text-3xl font-bold">الشروط والأحكام</h1>
        <p className="mt-2 text-xs text-white/30">آخر تحديث: يونيو 2026 · Last updated: June 2026</p>

        <div className="mt-10 space-y-8">
          {TERMS.map((t) => (
            <section key={t.title}>
              <h2 className="font-semibold text-amber-200 mb-2">{t.title}</h2>
              <p className="text-sm text-white/70 leading-relaxed">{t.body}</p>
            </section>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-sm text-white/60">
          <p className="font-medium text-white mb-2">Terms Summary (English)</p>
          <p>
            Services are scoped per contract. Monthly subscriptions cancel on 30 days notice. Setup
            fees refundable within 14 days if service hasn&apos;t started. All deliverables are yours.
            No guaranteed commercial outcomes — estimated results are estimates, not promises.
            Governed by Saudi law. Questions?{" "}
            <Link href="/contact" className="text-amber-300 hover:underline">
              Contact us
            </Link>
            .
          </p>
        </div>
      </div>
    </main>
  );
}
