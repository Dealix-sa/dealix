import Link from "next/link";
import { PREMIUM_OFFERS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Pricing — Dealix",
  description: "Seven strategic engagements, scoped to your company after a diagnostic call.",
};

export default function PricingPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Pricing</p>
          <h1 className="mt-3 text-4xl font-semibold">سبع أنظمة استراتيجية، ليست باقات جاهزة</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل نظام هنا مصمم لمشكلة تشغيلية حقيقية تُكلّف الشركة إيراداً أو وقتاً كل أسبوع تتأخر
            فيه. النطاق والسعر يُحددان بعد تشخيص سريع لحجم شركتك وحدة المشكلة — لا رقم عام يصلح
            للجميع، ولا شركة نجدها تحتاج نفس النطاق بالضبط.
          </p>
        </header>

        <section className="mt-10 overflow-hidden rounded-2xl border border-white/10">
          <table className="w-full text-sm">
            <thead className="bg-white/5 text-xs uppercase tracking-widest text-amber-300/80">
              <tr>
                <th className="px-4 py-3 text-left">Offer</th>
                <th className="px-4 py-3 text-left">لماذا لا تفوّته</th>
                <th className="px-4 py-3 text-left">الأنسب لـ</th>
              </tr>
            </thead>
            <tbody>
              {PREMIUM_OFFERS.map((o) => (
                <tr key={o.id} className="border-t border-white/10">
                  <td className="px-4 py-3 align-top">
                    <p className="font-medium">{o.name}</p>
                    <p className="text-xs text-white/60">{o.nameAr}</p>
                  </td>
                  <td className="px-4 py-3 align-top text-white/80">{o.positioningAr}</td>
                  <td className="px-4 py-3 align-top text-xs text-white/60">{o.bestFor.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="mt-8 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-6 text-sm text-white/80">
          <p className="font-medium text-amber-200">قواعد التسعير</p>
          <ul className="mt-2 space-y-1">
            <li>• لا رقم يُنشر بدون تشخيص — أي سعر مذكور خارج هذه الصفحة قبل مكالمة تشخيصية غير معتمد.</li>
            <li>• كل setup قابل للاسترداد خلال 14 يوم إذا لم يثبت قيمته.</li>
            <li>• الاشتراك الشهري قابل للإلغاء بإشعار 30 يوم، بدون auto-renewal بصمت.</li>
          </ul>
        </section>

        <section className="mt-8 text-center">
          <Link
            href="/book"
            className="inline-block rounded-full bg-amber-300 px-8 py-3 text-sm font-semibold text-black transition hover:bg-amber-200"
          >
            احجز تشخيص واعرف السعر الفعلي لشركتك
          </Link>
        </section>
      </div>
    </main>
  );
}
