import type { Metadata } from "next";
import Link from "next/link";
import { promises as fs } from "fs";
import path from "path";
import { BrandTokensView } from "./BrandTokensView";

type PageProps = { params: Promise<{ locale: string }> };

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const { locale } = await params;
  const isAr = locale === "ar";
  return {
    title: isAr ? "دليل الهوية البصرية — Dealix" : "Brand Identity Guide — Dealix",
    description: isAr
      ? "الألوان، الخطوط، الشعار، وقواعد الاستخدام لـ Dealix Post-Lead Revenue OS."
      : "Colors, typography, logo, and usage rules for the Dealix Post-Lead Revenue OS.",
  };
}

async function loadTokens() {
  const filePath = path.join(process.cwd(), "public", "brand", "tokens.json");
  const raw = await fs.readFile(filePath, "utf-8");
  return JSON.parse(raw) as Record<string, unknown>;
}

export default async function BrandGuidePage({ params }: PageProps) {
  const { locale } = await params;
  const isAr = locale === "ar";
  const base = `/${locale}`;
  const tokens = await loadTokens();

  return (
    <div className="min-h-screen bg-background" dir={isAr ? "rtl" : "ltr"}>
      <header className="border-b border-border/60">
        <div className="mx-auto max-w-5xl px-6 py-4 flex flex-wrap gap-4 text-sm">
          <Link href={base} className="text-muted-foreground hover:text-foreground">
            {isAr ? "← الرئيسية" : "← Home"}
          </Link>
          <a href="/brand/logo-mark.svg" download className="text-muted-foreground hover:text-foreground">
            {isAr ? "تنزيل الشعار (SVG)" : "Download mark (SVG)"}
          </a>
          <a href="/brand/logo-wordmark.svg" download className="text-muted-foreground hover:text-foreground">
            {isAr ? "تنزيل الـ wordmark" : "Download wordmark"}
          </a>
          <a href="/brand/tokens.json" download className="text-muted-foreground hover:text-foreground">
            tokens.json
          </a>
        </div>
      </header>

      <main className={`mx-auto max-w-5xl px-6 py-12 ${isAr ? "text-right" : "text-left"}`}>
        <h1 className="text-3xl font-bold">
          {isAr ? "دليل الهوية البصرية" : "Brand Identity Guide"}
        </h1>
        <p className="mt-3 text-muted-foreground leading-relaxed">
          {isAr
            ? "كل assets Dealix تتبع هذا الدليل. النصوص قابلة للنسخ بنقرة، والملفات قابلة للتنزيل."
            : "Every Dealix asset follows this guide. Token values copy on click; assets download directly."}
        </p>

        <BrandTokensView tokens={tokens} locale={locale} />
      </main>
    </div>
  );
}
