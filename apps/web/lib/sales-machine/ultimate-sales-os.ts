// Ultimate Sales OS — premium-page data layer.
// Offer pricing is derived from the canonical ladder in
// lib/offers/canonical-offers.ts — edit prices there, not here.

import {
  CANONICAL_OFFERS,
  type CanonicalOffer,
} from "@/lib/offers/canonical-offers";

export interface PremiumOffer {
  id: string;
  name: string;
  nameAr: string;
  setup: string;
  monthly: string;
  positioning: string;
  positioningAr: string;
  bestFor: string[];
}

const POSITIONING_EN: Record<CanonicalOffer["id"], string> = {
  free_diagnostic: "30-min workflow review. No obligation, no spam.",
  micro_sprint: "One fast, tangible fix delivered in 1–2 days to prove capability.",
  data_pack: "Qualified, classified prospect database ready for outreach.",
  managed_ops: "Daily AI operations with a weekly proof report and monthly founder review.",
  transformation_sprint:
    "Workflow map, leakage map, KPI model, and an implementation quote in 3–7 days.",
  custom_enterprise: "Custom-built AI system integrated with your team and tools.",
};

function toPremium(o: CanonicalOffer): PremiumOffer {
  return {
    id: o.id,
    name: o.name,
    nameAr: o.nameAr,
    setup: o.billing === "monthly" ? "—" : o.priceEn,
    monthly: o.billing === "monthly" ? o.priceEn : "—",
    positioning: POSITIONING_EN[o.id],
    positioningAr: o.description,
    bestFor: o.bestFor,
  };
}

export const PREMIUM_OFFERS: PremiumOffer[] = CANONICAL_OFFERS.map(toPremium);

export interface IndustryPlay {
  id: string;
  industry: string;
  industryAr: string;
  visibleSignals: string[];
  weaknesses: string[];
  bestOffer: string;
  openerAr: string;
  openerEn: string;
  proofAngle: string;
  first7DayWin: string;
}

export const INDUSTRY_PLAYS: IndustryPlay[] = [
  {
    id: "agency",
    industry: "Marketing Agency",
    industryAr: "وكالة تسويق",
    visibleSignals: ["Slow response to inbound", "Multiple ad accounts", "Founder approves every deliverable"],
    weaknesses: ["Lead response time", "Reporting cadence", "Capacity planning"],
    bestOffer: "Managed AI Operations (rung 4)",
    openerAr: "شفت إنكم تشتغلون على حملات قوية، بس الاستجابة على الليدز الواردة تتأخر. هذا اللي Dealix يحلّه.",
    openerEn: "I noticed you ship strong campaigns but inbound response is slow. Dealix closes that window.",
    proofAngle: "Weekly proof report on response time and qualified meetings.",
    first7DayWin: "Set up the response window + draft 3 outreach templates.",
  },
  {
    id: "training",
    industry: "Training / Consulting",
    industryAr: "تدريب / استشارات",
    visibleSignals: ["Public courses and events", "Speakers post content", "Trainers are the bottleneck"],
    weaknesses: ["Cohort follow-up", "Renewal cycle", "Trainer utilization"],
    bestOffer: "Transformation Diagnostic Sprint (rung 5)",
    openerAr: "لاحظت إن دوراتكم ممتازة، بس المتابعة بعد انتهاء الكورس ضعيفة. Dealix يبني نظام متابعة قابل للقياس.",
    openerEn: "Your courses are excellent, but post-course follow-up is light. Dealix builds a measurable retention flow.",
    proofAngle: "Renewal rate + NPS after first 60 days.",
    first7DayWin: "Map the cohort journey + draft renewal nudges.",
  },
  {
    id: "clinic",
    industry: "Clinic / Local Service",
    industryAr: "عيادة / خدمة محلية",
    visibleSignals: ["Google reviews", "Walk-in dominant", "Phone-first booking"],
    weaknesses: ["No-show rate", "Reputation response", "Recall cadence"],
    bestOffer: "Micro Sprint → Managed AI Operations (rungs 2→4)",
    openerAr: "تقييماتكم على Google تحتاج متابعة منتظمة. Dealix يبني نظام ردود بموافقة بشرية + تقرير شهري.",
    openerEn: "Your Google reviews need a steady response system. Dealix installs human-approved replies + a monthly report.",
    proofAngle: "Average rating + response rate after 60 days.",
    first7DayWin: "Audit reviews + draft 10 reply templates.",
  },
  {
    id: "real_estate",
    industry: "Real Estate Brokerage",
    industryAr: "وسطاء عقاريون",
    visibleSignals: ["Multiple listings", "Agent-only follow-up", "Heavy ad spend"],
    weaknesses: ["Lead-to-viewing ratio", "Agent consistency", "Listing promotion"],
    bestOffer: "Transformation Diagnostic Sprint (rung 5)",
    openerAr: "لاحظت إن العقارات تتغير بسرعة، بس المتابعة على الليدز مو منتظمة. Dealix ينسّق المتابعة على مستوى المكتب.",
    openerEn: "Listings change fast but follow-up isn't consistent. Dealix coordinates follow-up across the office.",
    proofAngle: "Lead-to-viewing + agent response time.",
    first7DayWin: "Standardize the lead routing rules + draft agent follow-ups.",
  },
  {
    id: "logistics",
    industry: "Logistics / B2B Services",
    industryAr: "لوجستيات / خدمات B2B",
    visibleSignals: ["B2B contracts", "Manual dispatch", "Phone + WhatsApp"],
    weaknesses: ["Dispatch visibility", "Customer updates", "SLA reporting"],
    bestOffer: "Managed AI Operations (rung 4)",
    openerAr: "أعرف إن التحديثات على الشحنات تكون يد. Dealix يبني غرفة قيادة بخمسة مؤشرات فقط.",
    openerEn: "I know shipment updates are manual. Dealix builds a command center with five KPIs only.",
    proofAngle: "On-time delivery + customer update SLA.",
    first7DayWin: "Map the dispatch workflow + define the 5 KPIs.",
  },
  {
    id: "consulting",
    industry: "Consulting Firm",
    industryAr: "مكتب استشاري",
    visibleSignals: ["Senior-led", "Engagement-based", "Long sales cycle"],
    weaknesses: ["Pipeline visibility", "Engagement reporting", "Senior time allocation"],
    bestOffer: "Managed AI Operations (rung 4)",
    openerAr: "شفت إن Pipeline عندكم ما عنده إيقاع أسبوعي. Dealix يركّب الإيقاع + تقرير إثبات أسبوعي.",
    openerEn: "Your pipeline doesn't have a weekly cadence. Dealix installs the cadence + a weekly proof report.",
    proofAngle: "Pipeline velocity + senior utilization.",
    first7DayWin: "Define the 5 KPIs + weekly review template.",
  },
];

export interface PremiumPillar {
  id: string;
  title: string;
  titleAr: string;
  problem: string;
  problemAr: string;
  solution: string;
  solutionAr: string;
  whatYouGet: string[];
  whatYouGetAr: string[];
  proofAngle: string;
  cta: string;
}

export const PREMIUM_PILLARS: PremiumPillar[] = [
  {
    id: "command_center",
    title: "Command Center",
    titleAr: "غرفة القيادة",
    problem: "Too many dashboards, no daily decision.",
    problemAr: "داشبورد كثيرة، بدون قرار يومي.",
    solution: "One page. Five KPIs. One owner per metric. One weekly review.",
    solutionAr: "صفحة واحدة. خمسة مؤشرات. مالك لكل مؤشر. مراجعة أسبوعية واحدة.",
    whatYouGet: [
      "Command Center URL with 5 modules",
      "Owners assigned per metric",
      "Daily standup template",
      "Weekly review template",
    ],
    whatYouGetAr: [
      "رابط غرفة القيادة بـ 5 وحدات",
      "تعيين مالك لكل مؤشر",
      "قالب standup يومي",
      "قالب مراجعة أسبوعية",
    ],
    proofAngle: "Daily decision velocity + weekly review adoption rate.",
    cta: "احجز مراجعة 20 دقيقة",
  },
  {
    id: "revenue_os",
    title: "Revenue OS",
    titleAr: "نظام الإيراد",
    problem: "Inbound leads fall through the cracks.",
    problemAr: "الليدز الواردة تضيع في الفوضى.",
    solution: "Lead routing, draft outreach, human-review queue, and follow-up cadence.",
    solutionAr: "توجيه ليدز، مسوّدة تواصل، طابور مراجعة بشرية، إيقاع متابعة.",
    whatYouGet: [
      "Lead routing rules",
      "Bilingual outreach drafts",
      "Human-review queue (no auto-send)",
      "Follow-up cadence",
    ],
    whatYouGetAr: [
      "قواعد توجيه الليدز",
      "مسوّدة تواصل عربي/إنجليزي",
      "طابور مراجعة بشرية (بدون auto-send)",
      "إيقاع متابعة",
    ],
    proofAngle: "Lead-to-meeting + meeting-to-close conversion.",
    cta: "شوف العرض المناسب",
  },
  {
    id: "review_reputation",
    title: "Review & Reputation OS",
    titleAr: "نظام السمعة",
    problem: "Reviews are scattered and reply-less.",
    problemAr: "التقييمات متفرقة وما أحد يرد.",
    solution: "Monitoring, human-approved replies, monthly report.",
    solutionAr: "مراقبة، ردود بموافقة بشرية، تقرير شهري.",
    whatYouGet: [
      "Review monitoring (Google/Maps)",
      "Reply templates (Arabic + English)",
      "Monthly reputation report",
      "Sentiment trends",
    ],
    whatYouGetAr: [
      "مراقبة تقييمات Google/Maps",
      "قوالب رد عربي وإنجليزي",
      "تقرير سمعة شهري",
      "اتجاهات sentiment",
    ],
    proofAngle: "Average rating + response rate over 90 days.",
    cta: "ابدأ التشخيص",
  },
  {
    id: "delivery_os",
    title: "Delivery OS",
    titleAr: "نظام التسليم",
    problem: "Client work happens but the client sees none of it.",
    problemAr: "الشغل عند العميل موجود، لكن العميل ما يشوف شي.",
    solution: "Workflow map, automation build, weekly proof, retention engine.",
    solutionAr: "خريطة عمل، بناء أتمتة، إثبات أسبوعي، محرك احتفاظ.",
    whatYouGet: [
      "Workflow map (as-is + to-be)",
      "Top 3 automations built",
      "Weekly proof report",
      "Retention + expansion playbook",
    ],
    whatYouGetAr: [
      "خريطة عمل (الحالي والمستهدف)",
      "بناء أفضل 3 أتمتة",
      "تقرير إثبات أسبوعي",
      "دليل احتفاظ وتوسعة",
    ],
    proofAngle: "Retention rate + expansion revenue per account.",
    cta: "احجز مكالمة 20 دقيقة",
  },
];

export function ultimatePackJson(date: string) {
  return {
    date,
    generatedAt: new Date().toISOString(),
    offers: PREMIUM_OFFERS,
    industries: INDUSTRY_PLAYS,
    pillars: PREMIUM_PILLARS,
    safety: { noAutoSend: true, humanReviewRequired: true, noFakeROI: true, noFakeTestimonials: true },
  };
}
