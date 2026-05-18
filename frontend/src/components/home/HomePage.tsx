import Link from "next/link";
import { getTranslations } from "next-intl/server";
import { PublicShell } from "@/components/layout/PublicShell";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Shield,
  TrendingUp,
  Bot,
  FileCheck,
  ArrowLeft,
  ArrowRight,
  Sparkles,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface HomePageProps {
  locale: string;
}

export async function HomePage({ locale }: HomePageProps) {
  const t = await getTranslations("home");
  const isAr = locale === "ar";
  const Arrow = isAr ? ArrowLeft : ArrowRight;

  const pillars = [
    {
      icon: TrendingUp,
      title: t("pillars.revenue.title"),
      body: t("pillars.revenue.body"),
    },
    {
      icon: Shield,
      title: t("pillars.governance.title"),
      body: t("pillars.governance.body"),
    },
    {
      icon: Bot,
      title: t("pillars.agents.title"),
      body: t("pillars.agents.body"),
    },
    {
      icon: FileCheck,
      title: t("pillars.proof.title"),
      body: t("pillars.proof.body"),
    },
  ];

  const offers = [
    {
      name: t("offers.diagnostic.name"),
      price: t("offers.diagnostic.price"),
      href: `/${locale}/login`,
    },
    {
      name: t("offers.sprint.name"),
      price: t("offers.sprint.price"),
      href: `/${locale}/offer/lead-intelligence-sprint`,
    },
    {
      name: t("offers.ops.name"),
      price: t("offers.ops.price"),
      href: `/${locale}/services`,
    },
  ];

  return (
    <PublicShell>
      <section
        className="relative overflow-hidden border-b border-border/50"
        dir={isAr ? "rtl" : "ltr"}
      >
        <div className="absolute inset-0 bg-gradient-to-br from-secondary/20 via-background to-primary/5 pointer-events-none" />
        <div className="page-container relative px-6 py-20 md:py-28 max-w-5xl mx-auto">
          <p className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-semibold text-primary mb-6">
            <Sparkles className="w-3.5 h-3.5" aria-hidden />
            {t("eyebrow")}
          </p>
          <h1
            className={cn(
              "text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-foreground font-display leading-[1.15]",
              isAr ? "text-right" : "text-left",
            )}
          >
            <span className="text-gradient-gold">{t("headlineAccent")}</span>
            <br />
            {t("headline")}
          </h1>
          <p
            className={cn(
              "mt-6 text-lg md:text-xl text-muted-foreground leading-relaxed max-w-2xl",
              isAr ? "text-right ms-auto" : "text-left",
            )}
          >
            {t("subhead")}
          </p>
          <div
            className={cn(
              "mt-10 flex flex-wrap gap-4",
              isAr ? "justify-end" : "justify-start",
            )}
          >
            <Button variant="gold" size="lg" asChild>
              <Link href={`/${locale}/dashboard`}>
                {t("ctaPrimary")}
                <Arrow className="w-4 h-4" />
              </Link>
            </Button>
            <Button variant="outline" size="lg" asChild>
              <Link href={`/${locale}/services`}>{t("ctaSecondary")}</Link>
            </Button>
          </div>
          <p className="mt-6 text-xs text-muted-foreground">{t("trustLine")}</p>
        </div>
      </section>

      <section className="page-container px-6 py-16 md:py-20" dir={isAr ? "rtl" : "ltr"}>
        <h2 className="text-2xl md:text-3xl font-bold text-center font-display mb-3">
          {t("pillarsTitle")}
        </h2>
        <p className="text-center text-muted-foreground max-w-2xl mx-auto mb-12">
          {t("pillarsSubtitle")}
        </p>
        <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {pillars.map(({ icon: Icon, title, body }) => (
            <Card
              key={title}
              className="card-glass border-border/70 hover:border-primary/40 transition-colors group"
            >
              <CardContent className="p-6">
                <div className="w-11 h-11 rounded-xl bg-primary/15 flex items-center justify-center mb-4 group-hover:scale-105 transition-transform">
                  <Icon className="w-5 h-5 text-primary" aria-hidden />
                </div>
                <h3 className="font-semibold text-foreground mb-2">{title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{body}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      <section
        className="border-y border-border/50 bg-card/30 py-16 md:py-20"
        dir={isAr ? "rtl" : "ltr"}
      >
        <div className="page-container px-6 max-w-4xl mx-auto text-center">
          <h2 className="text-2xl font-bold font-display mb-10">{t("offersTitle")}</h2>
          <div className="grid md:grid-cols-3 gap-4 text-start">
            {offers.map((offer, i) => (
              <Link
                key={offer.name}
                href={offer.href}
                className={cn(
                  "rounded-2xl border p-6 transition-all hover:shadow-lg",
                  i === 1
                    ? "border-primary bg-primary/5 scale-[1.02] shadow-md card-glow-gold"
                    : "border-border bg-card/60 hover:border-primary/30",
                )}
              >
                <p className="text-xs font-semibold uppercase tracking-wider text-primary mb-2">
                  {offer.price}
                </p>
                <p className="font-semibold text-foreground">{offer.name}</p>
              </Link>
            ))}
          </div>
        </div>
      </section>

      <section className="page-container px-6 py-16 md:py-24" dir={isAr ? "rtl" : "ltr"}>
        <div className="rounded-3xl border border-border bg-gradient-to-br from-secondary to-secondary/80 p-8 md:p-12 text-secondary-foreground text-center md:text-start flex flex-col md:flex-row md:items-center md:justify-between gap-8">
          <div className={cn("max-w-xl", isAr && "md:text-right")}>
            <h2 className="text-2xl md:text-3xl font-bold font-display text-white">
              {t("founderCtaTitle")}
            </h2>
            <p className="mt-3 text-white/85 leading-relaxed">{t("founderCtaBody")}</p>
          </div>
          <div className="flex flex-wrap gap-3 justify-center md:justify-end shrink-0">
            <Button variant="gold" size="lg" asChild>
              <Link href={`/${locale}/founder`}>{t("founderCtaBtn")}</Link>
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-white/40 text-white hover:bg-white/10"
              asChild
            >
              <Link href={`/${locale}/login`}>{t("loginCta")}</Link>
            </Button>
          </div>
        </div>
      </section>
    </PublicShell>
  );
}
