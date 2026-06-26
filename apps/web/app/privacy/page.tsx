import Link from "next/link";

export const metadata = {
  title: "سياسة الخصوصية — Dealix | Privacy Policy",
  description: "كيف نجمع بياناتك، نستخدمها، ونحميها — متوافق مع نظام PDPL السعودي.",
};

const SECTIONS_AR = [
  {
    title: "ما البيانات التي نجمعها؟",
    body: "نجمع فقط ما تزودنا به مباشرة: الاسم، الشركة، وسيلة التواصل (واتساب أو بريد إلكتروني)، ورسائلك عبر نماذج الموقع. لا نجمع بيانات تصفح تفصيلية أو نبيع بياناتك لأي طرف.",
  },
  {
    title: "كيف نستخدم بياناتك؟",
    body: "نستخدم بياناتك للرد على استفساراتك، إرسال عروض مطلوبة منك صراحةً، وتحسين خدماتنا. لا إرسال آلي بدون موافقتك. كل تواصل خارجي يمر بمراجعة المؤسس أولاً.",
  },
  {
    title: "مع من نشارك بياناتك؟",
    body: "لا نشارك بياناتك مع أطراف ثالثة إلا لضرورة تقنية (مزودو البنية التحتية كـ Railway) وبموجب اتفاقيات حماية بيانات. لا بيع، لا تأجير، لا مشاركة تسويقية.",
  },
  {
    title: "مدة الاحتفاظ بالبيانات",
    body: "نحتفظ ببياناتك طالما علاقتنا التجارية قائمة أو طالما يتطلب ذلك القانون. يمكنك طلب الحذف في أي وقت.",
  },
  {
    title: "حقوقك بموجب نظام PDPL",
    body: "وفقاً لنظام حماية البيانات الشخصية السعودي (PDPL)، يحق لك: الاطلاع على بياناتك، تصحيحها، طلب حذفها، والاعتراض على معالجتها. تواصل معنا عبر صفحة الاتصال.",
  },
  {
    title: "الأمان",
    body: "نستخدم تشفيراً قياسياً (HTTPS/TLS)، ونطبق مبدأ الحد الأدنى من البيانات — لا نجمع ما لا نحتاجه.",
  },
];

export default function PrivacyPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-3xl px-6 py-20">
        <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">
          سياسة الخصوصية · Privacy Policy
        </p>
        <h1 className="mt-4 text-3xl font-bold">سياسة الخصوصية</h1>
        <p className="mt-2 text-xs text-white/30">آخر تحديث: يونيو 2026 · Last updated: June 2026</p>

        <div className="mt-10 space-y-8">
          {SECTIONS_AR.map((s) => (
            <section key={s.title}>
              <h2 className="font-semibold text-amber-200 mb-2">{s.title}</h2>
              <p className="text-sm text-white/70 leading-relaxed">{s.body}</p>
            </section>
          ))}
        </div>

        <div className="mt-12 rounded-2xl border border-white/10 bg-white/[0.03] p-6 text-sm text-white/60">
          <p className="font-medium text-white mb-2">Privacy Policy (English Summary)</p>
          <p>
            We collect only what you provide (name, company, contact info, messages). We do not sell
            your data, share it with third parties beyond infrastructure providers, or send automated
            communications without your consent. You have the right to access, correct, or delete your
            data under Saudi PDPL. Contact us at the{" "}
            <Link href="/contact" className="text-amber-300 hover:underline">
              contact page
            </Link>
            .
          </p>
        </div>

        <p className="mt-8 text-xs text-white/30 text-center">
          للأسئلة:{" "}
          <Link href="/contact" className="text-amber-300 hover:underline">
            تواصل معنا
          </Link>
        </p>
      </div>
    </main>
  );
}
