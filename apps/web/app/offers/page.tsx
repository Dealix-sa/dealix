import Link from "next/link";
import { PREMIUM_OFFERS } from "@/lib/sales-machine/ultimate-sales-os";

export const metadata = {
  title: "Offers — Dealix",
  description: "Seven strategic engagements, from a free diagnostic to a custom enterprise system.",
};

export default function OffersPage() {
  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-6xl px-6 py-16">
        <header>
          <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">Offer Ladder</p>
          <h1 className="mt-3 text-4xl font-semibold">سبع عروض استراتيجية، ليست باقات عامة</h1>
          <p className="mt-3 max-w-2xl text-sm text-white/70">
            كل عميل يدخل من التشخيص المجاني، ونقرر مع بعض أي عرض يناسب حجم شركته وحدة المشكلة
            بالضبط. هذي ليست قائمة أسعار جاهزة — كل عرض هنا يستحق أن تفهمه قبل ما تفوّته.
          </p>
        </header>

        <section className="mt-10 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {PREMIUM_OFFERS.map((o) => (
            <article key={o.id} className="flex flex-col rounded-2xl border border-white/10 bg-white/5 p-6">
              <p className="text-xs uppercase tracking-widest text-amber-300/80">{o.id}</p>
              <h2 className="mt-2 text-xl font-semibold">{o.name}</h2>
              <p className="text-xs text-white/60">{o.nameAr}</p>
              <p className="mt-4 text-sm text-white/80">{o.positioning}</p>
              <p className="text-xs text-white/60">{o.positioningAr}</p>
              <ul className="mt-4 flex flex-wrap gap-2 text-[10px] text-white/60">
                {o.bestFor.map((b) => (
                  <li key={b} className="rounded-full border border-white/10 px-2 py-1">
                    {b}
                  </li>
                ))}
              </ul>
              <Link
                href="/book"
                className="mt-5 text-xs font-medium text-amber-300 hover:underline"
              >
                اعرف نطاقه وسعره الفعلي ←
              </Link>
            </article>
          ))}
        </section>
      </div>
    </main>
  );
}
