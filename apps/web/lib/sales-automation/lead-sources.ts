// Sales Automation — Lead sources, persuasion angles, and offer ladder
// Used by /automated-sales, /persuasion-room, /api/sales-machine/daily-pack

export type LeadSourceType =
  | "open_data"
  | "csv_import"
  | "manual_research"
  | "website_signal"
  | "google_places_official"
  | "hubspot_official"
  | "whatsapp_business_official"
  | "referral_warm";

export interface LeadSource {
  id: LeadSourceType;
  label: string;
  labelAr: string;
  description: string;
  descriptionAr: string;
  use: string;
  useAr: string;
  guardrails: string[];
  officialOnly: boolean;
  autoSendAllowed: boolean;
}

export interface PersuasionAngle {
  id: string;
  title: string;
  titleAr: string;
  signal: string;
  signalAr: string;
  hook: string;
  hookAr: string;
  bestFor: string[];
}

export interface OfferTier {
  id: string;
  name: string;
  nameAr: string;
  price: string;
  setup: string;
  setupAr: string;
  positioning: string;
  positioningAr: string;
}

export const LEAD_SOURCES: LeadSource[] = [
  {
    id: "open_data",
    label: "Saudi Open Data (Official)",
    labelAr: "البيانات المفتوحة السعودية (رسمي)",
    description:
      "Public datasets from data.gov.sa — sector mix, commercial registrations, economic indicators. No personal data scraped.",
    descriptionAr:
      "مجموعات بيانات عامة من data.gov.sa — مزيج قطاعات، سجلات تجارية، مؤشرات اقتصادية. لا يوجد تجريف لبيانات شخصية.",
    use: "Discover sectors + build segment hypothesis, never individual profiles.",
    useAr: "اكتشاف القطاعات وبناء فرضيات، وليس بناء ملفات شخصية.",
    guardrails: ["Use only public aggregate data", "No re-identification", "Cite source in every lead record"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "csv_import",
    label: "Local CSV Import",
    labelAr: "استيراد CSV محلي",
    description: "Founder-supplied CSV from approved public sources (events, partners, conferences).",
    descriptionAr: "ملف CSV يقدمه المؤسس من مصادر عامة موافق عليها (فعاليات، شركاء، مؤتمرات).",
    use: "Bulk upload + normalize + score.",
    useAr: "رفع جماعي + تطبيع + تسجيل نقاط.",
    guardrails: ["Source URL/note required", "No private lists", "Sample audit on first 10 rows"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "manual_research",
    label: "Manual Research (Funder Verified)",
    labelAr: "بحث يدوي (يتحقق منه المؤسس)",
    description: "Founder reads public sites, social posts, and ads; saves a structured note.",
    descriptionAr: "المؤسس يقرأ المواقع العامة والمنشورات والإعلانات ويحفظ ملاحظة مهيكلة.",
    use: "Highest trust. Slow but premium.",
    useAr: "أعلى ثقة. بطيء لكن premium.",
    guardrails: ["One source per lead", "URL/quote required", "Reviewed weekly"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "website_signal",
    label: "Website Signal Analyzer (Local File)",
    labelAr: "محلل إشارات الموقع (ملف محلي)",
    description:
      "Reads a manually saved HTML/text snapshot. Detects missing booking, unclear CTAs, no case studies.",
    descriptionAr:
      "يقرأ لقطة HTML/نص محفوظة يدوياً. يكتشف غياب الحجز، CTAs غير واضحة، عدم وجود دراسات حالة.",
    use: "Score a specific site without crawling the internet.",
    useAr: "تقييم موقع محدد بدون زحف للإنترنت.",
    guardrails: ["Manual file drop", "No crawling", "No form submission"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "google_places_official",
    label: "Google Places API (Official Plan)",
    labelAr: "Google Places API (خطة رسمية)",
    description: "Plan only. Public business info, ratings, hours. Never personal data.",
    descriptionAr: "خطة فقط. معلومات عامة، تقييمات، ساعات. لا بيانات شخصية.",
    use: "Verify the public surface of a candidate account.",
    useAr: "التحقق من السطح العام لحساب مرشح.",
    guardrails: ["Requires GOOGLE_PLACES_API_KEY", "Rate-limit aware", "Cache for 7 days"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "hubspot_official",
    label: "HubSpot CRM (Official Plan)",
    labelAr: "HubSpot CRM (خطة رسمية)",
    description: "Plan only. Sync deals/contacts from a HubSpot portal the client owns.",
    descriptionAr: "خطة فقط. مزامنة الصفقات/جهات الاتصال من بوابة HubSpot يملكها العميل.",
    use: "Read deals the founder is already managing.",
    useAr: "قراءة الصفقات اللي يديرها المؤسس أصلاً.",
    guardrails: ["OAuth scope minimal", "Read-only by default", "Token rotation quarterly"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "whatsapp_business_official",
    label: "WhatsApp Business (Official Plan)",
    labelAr: "WhatsApp Business (خطة رسمية)",
    description:
      "Plan only. Approved templates only. No scraping. Send only what the founder pre-approved.",
    descriptionAr:
      "خطة فقط. قوالب معتمدة فقط. لا تجريف. إرسال ما وافق عليه المؤسس مسبقاً فقط.",
    use: "Send approved drafts through official templates.",
    useAr: "إرسال المسودات المعتمدة عبر القوالب الرسمية.",
    guardrails: ["Templates pre-approved", "Opt-out respected", "No bulk unsolicited"],
    officialOnly: true,
    autoSendAllowed: false,
  },
  {
    id: "referral_warm",
    label: "Referral (Warm Intro)",
    labelAr: "إحالة (مقدمة دافئة)",
    description: "Founder or partner introduces a known contact with explicit consent.",
    descriptionAr: "المؤسس أو شريك يعرف شخصاً ويعطيه موافقة صريحة.",
    use: "Highest conversion, lowest volume.",
    useAr: "أعلى تحويل، أقل حجم.",
    guardrails: ["Written consent on first contact", "Source note saved"],
    officialOnly: true,
    autoSendAllowed: false,
  },
];

export const PERSUASION_ANGLES: PersuasionAngle[] = [
  {
    id: "leakage_to_revenue",
    title: "From leakage to revenue",
    titleAr: "من تسرّب إلى إيراد",
    signal: "Slow follow-up on inbound leads",
    signalAr: "متابعة بطيئة على الليدز الواردة",
    hook: "I noticed you ship fast on delivery but the response window to inbound leads is wide. Dealix closes that window with a 24/7 draft + human-review flow.",
    hookAr: "لاحظت إنكم تتسلمون بسرعة، لكن نافذة الرد على الليدز الواردة واسعة. Dealix يقفل النافذة بتدفّق مسوّدات 24/7 + مراجعة بشرية.",
    bestFor: ["marketing_agency", "consulting", "training"],
  },
  {
    id: "reputation_to_trust",
    title: "From scattered reviews to a trust wall",
    titleAr: "من تقييمات متفرقة إلى جدار ثقة",
    signal: "Reviews on Google/Maps are inconsistent",
    signalAr: "التقييمات على Google/Maps غير متجانسة",
    hook: "Your reviews are spread across platforms with no response system. Dealix turns that into a Review OS with weekly reports and human-approved replies.",
    hookAr: "تقييماتكم متفرقة بين المنصات بدون نظام رد. Dealix يحوّلها لـ Review OS بتقارير أسبوعية وردود بموافقة بشرية.",
    bestFor: ["clinic", "real_estate", "logistics"],
  },
  {
    id: "delivery_to_proof",
    title: "From delivery to proof",
    titleAr: "من تسليم إلى إثبات",
    signal: "No weekly report shared with client base",
    signalAr: "لا تقرير أسبوعي يُرسل لقاعدة العملاء",
    hook: "Your team does real work but the client sees none of it. Dealix turns that into a weekly proof report tied to each deliverable.",
    hookAr: "فريقكم يشتغل صح، لكن العميل ما يشوف شي. Dealix يحوّلها لتقرير إثبات أسبوعي مربوط بكل مخرج.",
    bestFor: ["b2b_services", "consulting", "agency"],
  },
  {
    id: "data_to_decision",
    title: "From data to a one-page decision",
    titleAr: "من بيانات إلى قرار على صفحة واحدة",
    signal: "Many dashboards, no daily decision",
    signalAr: "داشبورد كثيرة، بدون قرار يومي",
    hook: "You already have the data. Dealix gives you a one-page decision view for the founder, refreshed daily with human-verified numbers.",
    hookAr: "عندكم البيانات. Dealix يعطيك صفحة قرار واحدة للمؤسس، تتحدث يومياً بأرقام محققة.",
    bestFor: ["agency", "b2b_services", "logistics"],
  },
  {
    id: "ops_to_growth",
    title: "From operational chaos to growth capacity",
    titleAr: "من فوضى تشغيلية إلى طاقة نمو",
    signal: "Founder is the bottleneck on most decisions",
    signalAr: "المؤسس هو عنق الزجاجة في أغلب القرارات",
    hook: "If you take a 2-week vacation, the company slows down. Dealix installs the workflows so you don't have to be in the loop for every decision.",
    hookAr: "لو أخذت إجازة أسبوعين، الشركة تبطئ. Dealix يركّب الـ workflows بحيث ما تحتاج تكون في كل قرار.",
    bestFor: ["agency", "training", "b2b_services", "consulting"],
  },
];

export const OFFER_LADDER: OfferTier[] = [
  {
    id: "diagnostic_sprint",
    name: "Diagnostic Sprint",
    nameAr: "سباق تشخيصي",
    price: "Free / SAR 0",
    setup: "60-min workflow review, no obligation",
    setupAr: "مراجعة 60 دقيقة، بدون التزام",
    positioning: "Entry offer. We earn the right to propose.",
    positioningAr: "عرض الدخول. نكسب حق نقترح.",
  },
  {
    id: "revenue_os",
    name: "Revenue OS",
    nameAr: "نظام تشغيل الإيراد",
    price: "SAR 18,000 setup + SAR 5,000/mo",
    setup: "Lead flow + outreach drafts + weekly proof",
    setupAr: "تدفّق ليدز + مسوّدات تواصل + إثبات أسبوعي",
    positioning: "Best for agencies and B2B services with steady inbound.",
    positioningAr: "مناسب للوكالات وخدمات B2B ذات تدفق ثابت.",
  },
  {
    id: "command_center",
    name: "Command Center OS",
    nameAr: "نظام غرفة القيادة",
    price: "SAR 35,000 setup + SAR 9,000/mo",
    setup: "One-page decision view + 5 KPI owners + weekly review",
    setupAr: "صفحة قرار واحدة + 5 ملاك مؤشرات + مراجعة أسبوعية",
    positioning: "Best for founders who need clarity without more dashboards.",
    positioningAr: "مناسب للمؤسسين اللي يبغي وضوح بدون داشبورد زيادة.",
  },
  {
    id: "delivery_os",
    name: "Delivery OS",
    nameAr: "نظام تشغيل التسليم",
    price: "SAR 25,000 setup + SAR 6,000/mo",
    setup: "Workflow map + automation build + retention engine",
    setupAr: "خريطة عمل + بناء أتمتة + محرك احتفاظ",
    positioning: "Best for teams that have clients but no delivery OS.",
    positioningAr: "مناسب للفرق عندها عملاء، بس بدون نظام تسليم.",
  },
  {
    id: "review_reputation",
    name: "Review & Reputation OS",
    nameAr: "نظام تشغيل السمعة",
    price: "SAR 12,000 setup + SAR 3,500/mo",
    setup: "Review monitoring + reply drafts + monthly report",
    setupAr: "مراقبة تقييمات + مسوّدات رد + تقرير شهري",
    positioning: "Best for clinics, real estate, and local service operators.",
    positioningAr: "مناسب للعيادات والعقار ومشغلي الخدمات المحلية.",
  },
  {
    id: "custom_enterprise",
    name: "Custom Enterprise System",
    nameAr: "نظام مؤسسي مخصص",
    price: "SAR 80,000+ setup + SAR 18,000+/mo",
    setup: "Architecture, security, custom modules, dedicated ops",
    setupAr: "هندسة معمارية، أمان، وحدات مخصصة، عمليات مخصصة",
    positioning: "For groups with 50+ employees and multi-entity operations.",
    positioningAr: "للمجموعات فوق 50 موظف وعمليات متعددة الكيانات.",
  },
  {
    id: "managed_retainer",
    name: "Managed OS Retainer",
    nameAr: "اشتراك إدارة نظام",
    price: "SAR 4,000–12,000/mo",
    setup: "Ongoing ops, training, and quarterly reviews",
    setupAr: "عمليات مستمرة، تدريب، ومراجعات ربع سنوية",
    positioning: "For clients who need a partner, not a tool.",
    positioningAr: "للعملاء اللي يحتاجون شريك، مو أداة.",
  },
];

export const OUTREACH_OPENERS = {
  ar: [
    "مرحبًا [الاسم]، شفت إن [الشركة] تنشر محتوى قوي في [القطاع] بس الاستجابة على الليدز تأخذ وقت. هذا بالضبط اللي Dealix يحلّه — بدون spam، مع مراجعة بشرية.",
    "السلام عليكم، لاحظت إن موقعكم ما عنده مسار حجز واضح. Dealix يركّب المسار ويولّد المسوّدات، وأنتم توافقون قبل ما تنرسل.",
  ],
  en: [
    "Hi [Name], I noticed [Company] publishes strong work in [sector] but inbound response time is wide. Dealix closes that window with a draft + human-review flow — no spam.",
    "Hello, I saw your site doesn't surface a clear booking path. Dealix installs the path, drafts the messages, and only your team approves what goes out.",
  ],
};

export const OBJECTION_HANDLERS = [
  {
    objection: "We already have a CRM.",
    objectionAr: "عندنا CRM أصلاً.",
    response:
      "Dealix is not a CRM replacement. It's the layer that fills the CRM with verified drafts, follow-up queues, and proof reports — your CRM becomes the database, not the engine.",
    responseAr:
      "Dealix مو بديل CRM. هو الطبقة اللي تملأ CRM بمسوّدات محققة، طوابير متابعة، وتقارير إثبات — الـ CRM يصير قاعدة بيانات، مو محرك.",
  },
  {
    objection: "We tried AI tools before and they felt generic.",
    objectionAr: "جربنا أدوات ذكاء اصطناعي قبل وكانت عامة.",
    response:
      "That's exactly why every Dealix output carries a source note and a review gate. We do not send what a model generated blindly.",
    responseAr:
      "بالضبط لهذا السبب، كل مخرج من Dealix يحمل مصدر وبوابة مراجعة. ما نرسل شي مولّد أعمى.",
  },
  {
    objection: "Our team is small, we can't add another tool.",
    objectionAr: "فريقنا صغير، ما نقدر نضيف أداة زيادة.",
    response:
      "Dealix installs the workflow your team already has. The first 14 days are intake + map, not platform switch.",
    responseAr:
      "Dealix يركّب سير العمل اللي عندكم أصلاً. أول 14 يوم استلام وخريطة، مو تبديل منصة.",
  },
];

export function dailyPackMarkdown(date: string): string {
  const lines: string[] = [];
  lines.push(`# Dealix Daily Sales Machine Pack — ${date}`);
  lines.push("");
  lines.push("## Lead sources (official + safe)");
  for (const s of LEAD_SOURCES) {
    lines.push(`- **${s.label}** (${s.labelAr}) — auto_send=${s.autoSendAllowed ? "yes" : "no"}`);
  }
  lines.push("");
  lines.push("## Persuasion angles");
  for (const a of PERSUASION_ANGLES) {
    lines.push(`- **${a.title}** (${a.titleAr}) — ${a.signal}`);
  }
  lines.push("");
  lines.push("## Offer ladder");
  for (const o of OFFER_LADDER) {
    lines.push(`- **${o.name}** (${o.nameAr}) — ${o.price}`);
  }
  lines.push("");
  lines.push("## Arabic opener (safe template)");
  lines.push("> " + OUTREACH_OPENERS.ar[0]);
  lines.push("");
  lines.push("## English opener (safe template)");
  lines.push("> " + OUTREACH_OPENERS.en[0]);
  lines.push("");
  lines.push("---");
  lines.push("Drafts only. Human review required before any send. No auto-send.");
  return lines.join("\n");
}
