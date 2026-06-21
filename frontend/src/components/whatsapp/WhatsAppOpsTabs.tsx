import Link from "next/link";

const TABS = [
  { href: "", ar: "نظرة عامة", en: "Overview" },
  { href: "/sessions", ar: "الجلسات", en: "Sessions" },
  { href: "/action-cards", ar: "الكروت", en: "Action cards" },
  { href: "/assessments", ar: "التقييمات", en: "Assessments" },
];

export function WhatsAppOpsTabs({ locale, active }: { locale: string; active: string }) {
  const isAr = locale === "ar";
  return (
    <nav className="flex gap-2 flex-wrap mb-4">
      {TABS.map((t) => (
        <Link
          key={t.href || "overview"}
          href={`/${locale}/ops/whatsapp${t.href}`}
          className={`text-xs px-3 py-1.5 rounded-md border ${
            active === t.href
              ? "bg-foreground text-background border-foreground"
              : "border-border/80 text-muted-foreground"
          }`}
        >
          {isAr ? t.ar : t.en}
        </Link>
      ))}
    </nav>
  );
}
