import Link from "next/link";
import { CONTACT_EMAIL, mailtoLink } from "@/lib/contact";

const columns = [
  {
    title: "العروض",
    links: [
      { href: "/ar/offers", label: "سلم العروض الكامل" },
      { href: "/ar/pricing", label: "الأسعار" },
      { href: "/ar/diagnostic-sprint", label: "التشخيص التحولي" },
      { href: "/products", label: "الأنظمة" },
    ],
  },
  {
    title: "ابدأ",
    links: [
      { href: "/ar/intake", label: "التشخيص المجاني" },
      { href: "/contact", label: "تواصل معنا" },
      { href: "/ar/demo", label: "الديمو" },
    ],
  },
  {
    title: "الثقة",
    links: [
      { href: "/ar/trust", label: "حماية البيانات" },
      { href: "/ar/zatca-readiness", label: "جاهزية ZATCA" },
      { href: "/legal", label: "الشروط والخصوصية" },
      { href: "/safety", label: "الأمان" },
    ],
  },
];

// Shared footer for the public Arabic pages (rendered by app/ar/layout.tsx).
export default function ArFooter() {
  return (
    <footer dir="rtl" className="border-t border-white/10 bg-[#040d18]">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="grid gap-10 md:grid-cols-4">
          <div>
            <p className="text-xl font-black text-white">Dealix</p>
            <p className="mt-3 text-sm leading-7 text-slate-400">
              أنظمة تشغيل بالذكاء الاصطناعي للشركات السعودية — عربي أولاً،
              موافقة أولاً، بيانات حقيقية فقط.
            </p>
            <a
              href={mailtoLink("تواصل مع Dealix")}
              dir="ltr"
              className="mt-4 inline-block text-sm text-cyan-300 hover:underline"
            >
              {CONTACT_EMAIL}
            </a>
          </div>
          {columns.map((col) => (
            <div key={col.title}>
              <p className="text-sm font-black text-slate-200">{col.title}</p>
              <ul className="mt-3 space-y-2 text-sm text-slate-400">
                {col.links.map((l) => (
                  <li key={l.href}>
                    <Link href={l.href} className="transition-colors hover:text-cyan-300">
                      {l.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-white/5 pt-6 text-xs text-slate-500">
          <p>© 2026 Dealix · Saudi-first AI Business Operating Systems</p>
          <p>AI يكتب، أنت ترسل · لا إرسال تلقائي · PDPL-compliant</p>
        </div>
      </div>
    </footer>
  );
}
