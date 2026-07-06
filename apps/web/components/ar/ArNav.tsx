import Link from "next/link";

const links = [
  { href: "/ar", label: "الرئيسية" },
  { href: "/ar/offers", label: "العروض" },
  { href: "/ar/pricing", label: "الأسعار" },
  { href: "/ar/diagnostic-sprint", label: "التشخيص التحولي" },
  { href: "/ar/trust", label: "الثقة والحوكمة" },
  { href: "/contact", label: "تواصل" },
];

// Shared top navigation for the public Arabic pages (rendered by app/ar/layout.tsx).
export default function ArNav() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-[#06111f]/95 backdrop-blur">
      <nav
        dir="rtl"
        aria-label="التنقل الرئيسي"
        className="mx-auto flex max-w-6xl flex-wrap items-center gap-x-6 gap-y-2 px-6 py-4"
      >
        <Link href="/ar" className="text-xl font-black tracking-tight text-white">
          Dealix
        </Link>
        <ul className="flex flex-wrap items-center gap-x-5 gap-y-1 text-sm text-slate-300">
          {links.map((l) => (
            <li key={l.href}>
              <Link href={l.href} className="transition-colors hover:text-cyan-300">
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
        <Link
          href="/ar/intake"
          className="mr-auto rounded-xl bg-cyan-400 px-4 py-2 text-sm font-black text-[#06111f] transition-colors hover:bg-cyan-300"
        >
          ابدأ التشخيص المجاني
        </Link>
      </nav>
    </header>
  );
}
