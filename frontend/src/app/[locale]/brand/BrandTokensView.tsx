"use client";

import { useState } from "react";

interface ColorEntry {
  value: string;
  rgb?: number[];
  hsl?: number[];
  usage?: string;
}

interface BrandTokensViewProps {
  tokens: Record<string, unknown>;
  locale: string;
}

function isColorEntry(v: unknown): v is ColorEntry {
  return typeof v === "object" && v !== null && "value" in v;
}

export function BrandTokensView({ tokens, locale }: BrandTokensViewProps) {
  const isAr = locale === "ar";
  const [copied, setCopied] = useState<string | null>(null);

  function copy(text: string) {
    navigator.clipboard.writeText(text);
    setCopied(text);
    setTimeout(() => setCopied(null), 1200);
  }

  const color = tokens.color as Record<string, Record<string, unknown>>;
  const typo = tokens.typography as Record<string, unknown>;
  const rules = tokens.rules as { colorMix: string; forbidden: string[] };

  const allColorGroups: { key: string; titleAr: string; titleEn: string }[] = [
    { key: "primary", titleAr: "الألوان الأساسية", titleEn: "Primary colors" },
    { key: "secondary", titleAr: "الألوان الثانوية", titleEn: "Secondary colors" },
    { key: "semantic", titleAr: "الألوان الدلالية", titleEn: "Semantic colors" },
  ];

  return (
    <div className="mt-12 space-y-14">
      {/* Logo block */}
      <section>
        <h2 className="text-xl font-semibold">{isAr ? "الشعار" : "Logo"}</h2>
        <div className="mt-6 grid gap-6 md:grid-cols-2">
          <div className="rounded-lg border border-border/60 bg-card/40 p-6 text-center">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/brand/logo-mark.svg" alt="Dealix mark" className="mx-auto h-32 w-32" />
            <p className="mt-3 text-sm text-muted-foreground">{isAr ? "الشعار المربع (mark)" : "Square mark"}</p>
          </div>
          <div className="rounded-lg border border-border/60 bg-card/40 p-6 text-center">
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img src="/brand/logo-wordmark.svg" alt="Dealix wordmark" className="mx-auto h-32" />
            <p className="mt-3 text-sm text-muted-foreground">{isAr ? "الشعار الأفقي (wordmark)" : "Horizontal wordmark"}</p>
          </div>
        </div>
      </section>

      {/* Colors */}
      {allColorGroups.map((group) => {
        const groupTokens = color[group.key];
        if (!groupTokens) return null;
        return (
          <section key={group.key}>
            <h2 className="text-xl font-semibold">{isAr ? group.titleAr : group.titleEn}</h2>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {Object.entries(groupTokens).map(([name, entry]) => {
                if (!isColorEntry(entry)) return null;
                return (
                  <button
                    key={name}
                    type="button"
                    onClick={() => copy(entry.value)}
                    className="group rounded-lg border border-border/60 bg-card/40 p-4 text-left transition hover:border-primary/60"
                  >
                    <div
                      className="h-16 w-full rounded"
                      style={{ background: entry.value }}
                    />
                    <div className="mt-3 flex items-center justify-between">
                      <span className="text-sm font-medium">{name}</span>
                      <code className="font-mono text-xs text-muted-foreground">
                        {copied === entry.value ? (isAr ? "نسخ ✓" : "copied ✓") : entry.value}
                      </code>
                    </div>
                    {entry.usage && (
                      <p className="mt-2 text-xs text-muted-foreground leading-relaxed">{entry.usage}</p>
                    )}
                  </button>
                );
              })}
            </div>
          </section>
        );
      })}

      {/* Typography */}
      <section>
        <h2 className="text-xl font-semibold">{isAr ? "الخطوط" : "Typography"}</h2>
        <div className="mt-6 grid gap-4 md:grid-cols-2">
          <div className="rounded-lg border border-border/60 bg-card/40 p-5">
            <p className="text-sm text-muted-foreground">Arabic primary</p>
            <p className="mt-2 text-2xl" style={{ fontFamily: "'IBM Plex Sans Arabic', system-ui" }}>
              أنا أبني نظام إيرادات يثبت ما بعد الـ lead.
            </p>
          </div>
          <div className="rounded-lg border border-border/60 bg-card/40 p-5">
            <p className="text-sm text-muted-foreground">English primary</p>
            <p className="mt-2 text-2xl" style={{ fontFamily: "Inter, system-ui" }}>
              Proving what happens after the lead.
            </p>
          </div>
        </div>
        <details className="mt-4 rounded-md border border-border/60 bg-card/20 px-4 py-3">
          <summary className="cursor-pointer text-sm font-medium">{isAr ? "تفاصيل الخطوط والمقاييس" : "Type scale and weights"}</summary>
          <pre className="mt-3 overflow-x-auto rounded bg-card/40 p-3 text-xs leading-relaxed">
{JSON.stringify(typo, null, 2)}
          </pre>
        </details>
      </section>

      {/* Rules */}
      <section>
        <h2 className="text-xl font-semibold">{isAr ? "قواعد الاستخدام" : "Usage rules"}</h2>
        <ul className="mt-4 space-y-2 text-sm leading-relaxed">
          <li>
            <strong>{isAr ? "خلطة الألوان: " : "Color mix: "}</strong>
            <span className="text-muted-foreground">{rules.colorMix}</span>
          </li>
          {rules.forbidden.map((rule, i) => (
            <li key={i} className="flex gap-2">
              <span className="text-destructive">✗</span>
              <span className="text-muted-foreground">{rule}</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
