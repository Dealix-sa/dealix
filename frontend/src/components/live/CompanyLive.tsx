/**
 * CompanyLive — the unified "Dealix يشتغل الآن / Dealix, Live" surface.
 *
 * Server Component: reads the governed snapshot (company_live.json) + bilingual
 * service copy (services_copy.json) at build time and renders the operating company
 * as a website — strongest services, today's scored pipeline, daily drafts, a manual
 * call list, a sample diagnostic, and gated proposals.
 *
 * Doctrine surfaced visually: every external action is a DRAFT awaiting founder
 * approval; nothing auto-sends; no fabricated leads (real-vs-seed labelled honestly).
 * The big JSON stays server-side — only rendered HTML reaches the client.
 */

import Link from "next/link";
import { PublicGtmShell } from "@/components/gtm/PublicGtmShell";
import snapshot from "@/content/company_live.json";
import servicesCopy from "@/content/services_copy.json";

type L = "ar" | "en";

interface Service {
  id: string;
  code: string;
  name: string;
  name_ar: string;
  tagline: string;
  category: string;
  price_min: number | null;
  price_max: number | null;
  is_monthly: boolean;
  duration_days: { min?: number; max?: number };
  deliverables: string[];
  pricing_note: string;
}
interface Lead {
  rank: number;
  company: string;
  contact: string;
  segment: string;
  motion: string;
  offer_id: string;
  pain: string;
  next_action: string;
  priority: string;
  score: number;
  tier: string;
  data_status: "real" | "seed_placeholder";
}
interface Draft {
  company: string;
  contact: string;
  channel: string;
  tone: string;
  subject: string;
  body_ar: string;
  body_en: string;
  approval_status: string;
  data_status: string;
}
interface Call {
  company: string;
  contact: string;
  objective_ar: string;
  objective_en: string;
  script_ar: string;
  script_en: string;
  phone_note: string;
  approval_status: string;
}
interface Proposal {
  company: string;
  offer_name: string;
  offer_name_ar: string;
  scope_summary_ar: string;
  price_band_sar: string;
  pricing_gate: string;
  approval_status: string;
}
interface DiagSection {
  title_ar: string;
  title_en: string;
  body_ar: string;
  body_en: string;
}
interface Snapshot {
  meta: {
    generated_at: string;
    doctrine: string[];
    counts: Record<string, number>;
    intake_hint: string;
  };
  services: Service[];
  pipeline: Lead[];
  drafts: Draft[];
  call_list: Call[];
  diagnostic_sample: { company: string; sector: string; sections: DiagSection[] } | null;
  proposals: Proposal[];
}
interface Copy {
  headline_ar: string;
  headline_en: string;
  subhead_ar: string;
  subhead_en: string;
  value_props_ar: string[];
  value_props_en: string[];
  who_for_ar: string;
  who_for_en: string;
  proof_angle_ar: string;
  proof_angle_en: string;
  cta_ar: string;
  cta_en: string;
}

const SNAP = snapshot as unknown as Snapshot;
const COPY = servicesCopy as unknown as Record<string, Copy>;

const T = {
  liveTitle: { ar: "Dealix تشتغل الآن", en: "Dealix, Live" },
  heroSub: {
    ar: "شركة خدمات ذكاء اصطناعي تعمل بمحرّكات حقيقية — أقوى الخدمات، خط أنابيب مُقيَّم، ومسودات يومية جاهزة لموافقتك. كل إجراء خارجي مسودة بانتظار موافقة المؤسس.",
    en: "An AI services company running on real engines — strongest services, a scored pipeline, and daily drafts ready for your approval. Every external action is a draft awaiting founder approval.",
  },
  services: { ar: "أقوى الخدمات", en: "Strongest Services" },
  servicesSub: {
    ar: "سلّم عروض يبني على الإثبات قبل التوسّع — من تدقيق منخفض المخاطر إلى أنظمة تشغيل كاملة.",
    en: "An offer ladder that builds on proof before scale — from a low-risk audit to full operating systems.",
  },
  today: { ar: "لوحة اليوم التشغيلية", en: "Today's Operating Board" },
  pipeline: { ar: "خط الأنابيب المُقيَّم", en: "Scored Pipeline" },
  pipelineSub: {
    ar: "مُرتّب بنظام تقييم شفّاف (0–100). العملاء الحقيقيون يتصدّرون؛ الأهداف الـ seed تُوسم بوضوح.",
    en: "Ranked by a transparent 0–100 score. Real leads lead; seeded targets are clearly labelled.",
  },
  drafts: { ar: "مسودات اليوم (بانتظار موافقتك)", en: "Today's Drafts (Awaiting Your Approval)" },
  calls: { ar: "قائمة الاتصال (اتصال يدوي)", en: "Call List (Manual Dial)" },
  diagnostic: { ar: "تشخيص نموذجي محكوم", en: "Governed Sample Diagnostic" },
  proposals: { ar: "عروض مُسوّدة (سعر بانتظار موافقة)", en: "Drafted Proposals (Price Gated)" },
  approval: { ar: "بانتظار موافقة", en: "Approval required" },
  manual: { ar: "اتصال يدوي من المؤسس", en: "Founder dials manually" },
  real: { ar: "عميل حقيقي", en: "Real lead" },
  seed: { ar: "هدف seed", en: "Seed target" },
  score: { ar: "التقييم", en: "Score" },
  next: { ar: "الخطوة التالية", en: "Next action" },
  whatsapp: { ar: "واتساب", en: "WhatsApp" },
  email: { ar: "بريد", en: "Email" },
  whoFor: { ar: "لمن؟", en: "Who for" },
  proofAngle: { ar: "كيف نُثبت", en: "How we prove it" },
  priceBand: { ar: "النطاق التقديري", en: "Estimated band" },
  scope: { ar: "النطاق", en: "Scope" },
  intakeTitle: { ar: "حمّل عملاءك الحقيقيين", en: "Load your real leads" },
  generated: { ar: "تم التوليد", en: "Generated" },
};

const COUNT_LABELS: Record<string, { ar: string; en: string }> = {
  services: { ar: "خدمة", en: "Services" },
  pipeline_total: { ar: "خط الأنابيب", en: "Pipeline" },
  real_leads: { ar: "عملاء حقيقيون", en: "Real leads" },
  seed_placeholders: { ar: "أهداف seed", en: "Seed targets" },
  drafts_queued: { ar: "مسودات جاهزة", en: "Drafts queued" },
  calls_queued: { ar: "مكالمات جاهزة", en: "Calls queued" },
  proposals_drafted: { ar: "عروض مُسوّدة", en: "Proposals" },
};

const CHANNEL_LABEL: Record<string, { ar: string; en: string }> = {
  whatsapp: T.whatsapp,
  email: T.email,
};

function fmtSar(min: number | null, max: number | null, monthly: boolean): string {
  if (!min || !max) return "—";
  const a = min.toLocaleString("en-US");
  const b = max.toLocaleString("en-US");
  return monthly ? `${a}–${b}/mo SAR` : `${a}–${b} SAR`;
}

export function CompanyLive({ locale }: { locale: string }) {
  const L: L = locale === "en" ? "en" : "ar";
  const ar = L === "ar";
  const pick = (o: { ar: string; en: string }) => (ar ? o.ar : o.en);
  const c = SNAP.meta.counts;
  const topPipeline = SNAP.pipeline.slice(0, 24);
  const shownDrafts = SNAP.drafts.slice(0, 12);

  const Chip = ({
    children,
    tone = "navy",
  }: {
    children: React.ReactNode;
    tone?: "navy" | "gold" | "emerald" | "amber" | "muted";
  }) => {
    const tones: Record<string, string> = {
      navy: "bg-navy-500/15 text-navy-200 border-navy-400/30",
      gold: "bg-gold-500/15 text-gold-300 border-gold-500/40",
      emerald: "bg-emerald-500/15 text-emerald-300 border-emerald-500/40",
      amber: "bg-amber-500/15 text-amber-300 border-amber-500/40",
      muted: "bg-white/5 text-white/60 border-white/10",
    };
    return (
      <span
        className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-0.5 text-xs font-medium ${tones[tone]}`}
      >
        {children}
      </span>
    );
  };

  const SectionTitle = ({
    title,
    sub,
    id,
  }: {
    title: { ar: string; en: string };
    sub?: { ar: string; en: string };
    id?: string;
  }) => (
    <div id={id} className="mb-6 scroll-mt-24">
      <h2 className="text-2xl font-bold text-white md:text-3xl">{pick(title)}</h2>
      {sub && <p className="mt-2 max-w-3xl text-sm text-white/60 md:text-base">{pick(sub)}</p>}
    </div>
  );

  return (
    <PublicGtmShell>
      <main className="min-h-screen bg-navy-950 text-white">
        {/* Hero */}
        <section className="border-b border-white/10 bg-gradient-to-b from-navy-700 to-navy-950 px-5 py-16 md:py-24">
          <div className="mx-auto max-w-6xl">
            <Chip tone="emerald">
              <span className="h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
              {ar ? "النظام يعمل" : "System live"}
            </Chip>
            <h1 className="mt-4 text-4xl font-extrabold leading-tight md:text-6xl">
              {pick(T.liveTitle)}
            </h1>
            <p className="mt-5 max-w-3xl text-base text-white/70 md:text-lg">{pick(T.heroSub)}</p>
            <div className="mt-8 flex flex-wrap gap-3">
              <a
                href="#services"
                className="rounded-xl bg-gold-500 px-6 py-3 text-sm font-bold text-navy-900 transition hover:bg-gold-400"
              >
                {pick(T.services)}
              </a>
              <a
                href="#today"
                className="rounded-xl border border-white/20 px-6 py-3 text-sm font-bold text-white transition hover:bg-white/5"
              >
                {pick(T.today)}
              </a>
            </div>
            <p className="mt-6 text-xs text-white/40">
              {pick(T.generated)}: {new Date(SNAP.meta.generated_at).toLocaleString(L)}
            </p>
          </div>
        </section>

        {/* Governance banner */}
        <section className="border-b border-white/10 bg-navy-900 px-5 py-8">
          <div className="mx-auto max-w-6xl">
            <div className="flex items-center gap-2 text-gold-300">
              <span aria-hidden>🛡️</span>
              <span className="text-sm font-bold">
                {ar ? "الحوكمة (قانون لا استثناء منه)" : "Governance (no-exception rules)"}
              </span>
            </div>
            <ul className="mt-3 grid gap-2 md:grid-cols-2">
              {SNAP.meta.doctrine.map((d, i) => (
                <li key={i} className="flex items-start gap-2 text-sm text-white/70">
                  <span className="mt-1 text-emerald-400" aria-hidden>
                    ✓
                  </span>
                  {d}
                </li>
              ))}
            </ul>
          </div>
        </section>

        {/* Today's board (counts) */}
        <section className="px-5 py-12">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.today} id="today" />
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4 lg:grid-cols-7">
              {Object.entries(COUNT_LABELS).map(([key, lbl]) => (
                <div
                  key={key}
                  className="rounded-2xl border border-white/10 bg-navy-900 p-4 text-center"
                >
                  <div className="text-3xl font-extrabold text-gold-400">{c[key] ?? 0}</div>
                  <div className="mt-1 text-xs text-white/60">{pick(lbl)}</div>
                </div>
              ))}
            </div>
            {c.real_leads === 0 && (
              <p className="mt-4 rounded-xl border border-amber-500/30 bg-amber-500/10 p-3 text-sm text-amber-200">
                {ar
                  ? "ملاحظة صادقة: 0 عملاء حقيقيين محمّلين بعد. الأرقام أدناه أهداف seed استراتيجية تُوسم بوضوح — النظام لا يخترع أحداً. حمّل بياناتك الحقيقية ليتصدّروا كل القوائم."
                  : "Honest note: 0 real leads loaded yet. The rows below are clearly-labelled strategic seed targets — the system fabricates no one. Load your real data and it leads every queue."}
              </p>
            )}
          </div>
        </section>

        {/* Strongest services */}
        <section className="border-t border-white/10 bg-navy-900/40 px-5 py-14">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.services} sub={T.servicesSub} id="services" />
            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {SNAP.services.map((s) => {
                const cp = COPY[s.id];
                const head = cp ? (ar ? cp.headline_ar : cp.headline_en) : ar ? s.name_ar : s.name;
                const sub = cp ? (ar ? cp.subhead_ar : cp.subhead_en) : s.tagline;
                const props = cp ? (ar ? cp.value_props_ar : cp.value_props_en) : s.deliverables;
                return (
                  <div
                    key={s.id}
                    className="flex flex-col rounded-2xl border border-white/10 bg-navy-950 p-6 transition hover:border-gold-500/40"
                  >
                    <div className="flex items-center justify-between">
                      <Chip tone="gold">{s.code}</Chip>
                      <span className="text-xs text-white/40">{s.category}</span>
                    </div>
                    <h3 className="mt-3 text-lg font-bold text-white">{head}</h3>
                    <p className="mt-2 text-sm text-white/60">{sub}</p>
                    <ul className="mt-4 space-y-1.5">
                      {props.slice(0, 3).map((p, i) => (
                        <li key={i} className="flex items-start gap-2 text-sm text-white/70">
                          <span className="mt-1 text-emerald-400" aria-hidden>
                            ◆
                          </span>
                          {p}
                        </li>
                      ))}
                    </ul>
                    {cp && (
                      <p className="mt-4 text-xs text-white/50">
                        <span className="font-semibold text-white/70">{pick(T.proofAngle)}: </span>
                        {ar ? cp.proof_angle_ar : cp.proof_angle_en}
                      </p>
                    )}
                    <div className="mt-auto pt-5">
                      <div className="flex items-center justify-between border-t border-white/10 pt-4">
                        <div>
                          <div className="text-xs text-white/40">{pick(T.priceBand)}</div>
                          <div className="text-sm font-bold text-gold-300">
                            {fmtSar(s.price_min, s.price_max, s.is_monthly)}
                          </div>
                        </div>
                        <Link
                          href={`/${L}/services`}
                          className="rounded-lg border border-gold-500/40 px-3 py-1.5 text-xs font-bold text-gold-300 transition hover:bg-gold-500/10"
                        >
                          {cp ? (ar ? cp.cta_ar : cp.cta_en) : ar ? "اعرف أكثر" : "Learn more"}
                        </Link>
                      </div>
                      <p className="mt-2 text-[11px] leading-snug text-white/35">{s.pricing_note}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </section>

        {/* Pipeline */}
        <section className="px-5 py-14">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.pipeline} sub={T.pipelineSub} id="pipeline" />
            <div className="overflow-hidden rounded-2xl border border-white/10">
              <table className="w-full text-start text-sm">
                <thead className="bg-navy-900 text-xs uppercase text-white/50">
                  <tr>
                    <th className="px-3 py-3 text-start">#</th>
                    <th className="px-3 py-3 text-start">{ar ? "الجهة" : "Company"}</th>
                    <th className="px-3 py-3 text-start">{ar ? "القطاع" : "Segment"}</th>
                    <th className="px-3 py-3 text-start">{pick(T.score)}</th>
                    <th className="hidden px-3 py-3 text-start md:table-cell">{pick(T.next)}</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/5">
                  {topPipeline.map((p) => (
                    <tr key={p.rank} className="bg-navy-950 hover:bg-navy-900/60">
                      <td className="px-3 py-3 text-white/40">{p.rank}</td>
                      <td className="px-3 py-3">
                        <div className="font-medium text-white">{p.company}</div>
                        <div className="mt-1">
                          <Chip tone={p.data_status === "real" ? "emerald" : "muted"}>
                            {p.data_status === "real" ? pick(T.real) : pick(T.seed)}
                          </Chip>
                        </div>
                      </td>
                      <td className="px-3 py-3 text-white/60">{p.segment || "—"}</td>
                      <td className="px-3 py-3">
                        <span className="font-bold text-gold-300">{p.score}</span>
                        <span className="text-white/30"> /100</span>
                        <div className="text-[11px] text-white/40">{p.tier}</div>
                      </td>
                      <td className="hidden px-3 py-3 text-white/60 md:table-cell">
                        {p.next_action || "—"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {SNAP.pipeline.length > topPipeline.length && (
              <p className="mt-3 text-xs text-white/40">
                {ar
                  ? `عرض أعلى ${topPipeline.length} من ${SNAP.pipeline.length}.`
                  : `Showing top ${topPipeline.length} of ${SNAP.pipeline.length}.`}
              </p>
            )}
          </div>
        </section>

        {/* Daily drafts */}
        <section className="border-t border-white/10 bg-navy-900/40 px-5 py-14">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.drafts} id="drafts" />
            <div className="grid gap-5 md:grid-cols-2">
              {shownDrafts.map((d, i) => (
                <div key={i} className="rounded-2xl border border-white/10 bg-navy-950 p-5">
                  <div className="flex flex-wrap items-center gap-2">
                    <Chip tone="navy">{pick(CHANNEL_LABEL[d.channel] ?? { ar: d.channel, en: d.channel })}</Chip>
                    <Chip tone="muted">{d.tone}</Chip>
                    <Chip tone="amber">⏸ {pick(T.approval)}</Chip>
                  </div>
                  <div className="mt-3 text-sm font-bold text-white">{d.company}</div>
                  {d.subject && <div className="mt-1 text-xs text-white/50">{d.subject}</div>}
                  <p className="mt-3 whitespace-pre-line text-sm text-white/75" dir="rtl">
                    {d.body_ar}
                  </p>
                  <details className="mt-2">
                    <summary className="cursor-pointer text-xs text-white/40">EN</summary>
                    <p className="mt-1 whitespace-pre-line text-sm text-white/55" dir="ltr">
                      {d.body_en}
                    </p>
                  </details>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Call list */}
        <section className="px-5 py-14">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.calls} id="calls" />
            <div className="grid gap-5 md:grid-cols-2">
              {SNAP.call_list.map((call, i) => (
                <div key={i} className="rounded-2xl border border-white/10 bg-navy-950 p-5">
                  <div className="flex items-center justify-between">
                    <div className="text-sm font-bold text-white">{call.company}</div>
                    <Chip tone="amber">📞 {pick(T.manual)}</Chip>
                  </div>
                  <div className="mt-1 text-xs text-white/50">{ar ? call.objective_ar : call.objective_en}</div>
                  <p className="mt-3 whitespace-pre-line text-sm text-white/75" dir={ar ? "rtl" : "ltr"}>
                    {ar ? call.script_ar : call.script_en}
                  </p>
                  <p className="mt-3 text-[11px] text-white/35">{call.phone_note}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Diagnostic sample */}
        {SNAP.diagnostic_sample && (
          <section className="border-t border-white/10 bg-navy-900/40 px-5 py-14">
            <div className="mx-auto max-w-6xl">
              <SectionTitle title={T.diagnostic} id="diagnostic" />
              <div className="rounded-2xl border border-white/10 bg-navy-950 p-6">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="text-lg font-bold text-white">{SNAP.diagnostic_sample.company}</span>
                  <Chip tone="navy">{SNAP.diagnostic_sample.sector}</Chip>
                  <Chip tone="amber">⏸ {pick(T.approval)}</Chip>
                </div>
                <div className="mt-5 grid gap-4 md:grid-cols-2">
                  {SNAP.diagnostic_sample.sections.map((sec, i) => (
                    <div key={i} className="rounded-xl border border-white/10 bg-navy-900 p-4">
                      <h4 className="text-sm font-bold text-gold-300">
                        {ar ? sec.title_ar : sec.title_en}
                      </h4>
                      <p className="mt-2 whitespace-pre-line text-sm text-white/65">
                        {ar ? sec.body_ar : sec.body_en}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Proposals */}
        <section className="px-5 py-14">
          <div className="mx-auto max-w-6xl">
            <SectionTitle title={T.proposals} id="proposals" />
            <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
              {SNAP.proposals.map((pr, i) => (
                <div key={i} className="rounded-2xl border border-white/10 bg-navy-950 p-5">
                  <div className="text-sm font-bold text-white">{pr.company}</div>
                  <div className="mt-1 text-xs text-gold-300">{ar ? pr.offer_name_ar : pr.offer_name}</div>
                  <p className="mt-3 text-sm text-white/65">{pr.scope_summary_ar}</p>
                  <div className="mt-4 border-t border-white/10 pt-3">
                    <div className="text-xs text-white/40">{pick(T.priceBand)}</div>
                    <div className="text-sm font-bold text-gold-300">{pr.price_band_sar}</div>
                    <p className="mt-2 text-[11px] text-white/35">{pr.pricing_gate}</p>
                  </div>
                  <div className="mt-3">
                    <Chip tone="amber">⏸ {pick(T.approval)}</Chip>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Intake / how to load real leads */}
        <section className="border-t border-white/10 bg-gradient-to-b from-navy-900 to-navy-950 px-5 py-14">
          <div className="mx-auto max-w-4xl rounded-2xl border border-gold-500/30 bg-navy-950 p-8">
            <h2 className="text-xl font-bold text-gold-300">{pick(T.intakeTitle)}</h2>
            <p className="mt-3 text-sm text-white/70">{SNAP.meta.intake_hint}</p>
            <pre className="mt-4 overflow-x-auto rounded-xl bg-black/40 p-4 text-xs text-emerald-300" dir="ltr">
{`# 1) ضع عملاءك الحقيقيين في:
docs/commercial/operations/targeting/agency_accounts_seed.csv

# 2) أعد توليد اللقطة الحية:
python3 scripts/build_company_live.py`}
            </pre>
            <p className="mt-4 text-xs text-white/40">
              {ar
                ? "النظام يقيّمهم، يرتّبهم، ويولّد مسودات + سكربتات اتصال — بانتظار موافقتك. لا إرسال تلقائي، لا أرقام مخترعة."
                : "The system scores, ranks, and drafts outreach + call scripts — awaiting your approval. No auto-send, no fabricated numbers."}
            </p>
          </div>
        </section>
      </main>
    </PublicGtmShell>
  );
}
