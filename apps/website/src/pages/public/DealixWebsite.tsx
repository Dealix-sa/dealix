type Lang = "ar" | "en";

const copy = {
  ar: {
    dir: "rtl",
    nav: ["المشكلة", "الأنظمة", "المنهجية", "المقارنة", "الباقات"],
    badge: "Company Brain + Revenue Command Room + Trust Gates",
    title: "نحوّل فوضى المبيعات والمتابعة إلى نظام تشغيل يومي للشركة.",
    lead:
      "Dealix تبني للشركات السعودية أنظمة تشغيل ذكاء اصطناعي تربط الإيراد، المتابعة، واتساب، العروض، التقارير، القرار الإداري، والحوكمة في workflow واضح وقابل للتنفيذ.",
    primary: "احجز تشخيص مجاني",
    secondary: "شاهد الأنظمة",
    panelTitle: "Dealix Command Room",
    live: "جاهز للتشغيل",
    metrics: [
      ["100", "شركة تُبحث يوميًا", "استهداف منضبط"],
      ["25", "مسودة جاهزة", "مراجعة بشرية"],
      ["10", "إرسال يدوي", "بدون عشوائية"],
      ["1", "قرار يومي", "للإدارة"]
    ],
    decision:
      "قرار اليوم: ابدأ بقطاع واحد، راجع 25 فرصة، أرسل 10 رسائل فقط، وادفع 3 مكالمات تشخيص.",
    problemTitle: "الشركات لا ينقصها أدوات. ينقصها نظام تشغيل.",
    problemText:
      "الأدوات موجودة، لكن الفرص تضيع بين واتساب، الإيميل، الموظفين، العروض، والتقارير. Dealix يبني طبقة تشغيل فوق الموجود حتى يعرف المالك ماذا يحدث وماذا يفعل اليوم.",
    problems: [
      ["فرص تضيع", "عملاء يسألون ثم يختفون لأن المتابعة غير موحدة."],
      ["واتساب خارج القياس", "محادثات مهمة بلا تصنيف، بلا owner، وبلا next action."],
      ["تقارير بلا قرار", "أرقام كثيرة، لكن لا يوجد قرار يومي واضح."],
      ["AI بلا حوكمة", "استخدام أدوات ذكاء اصطناعي بدون سياسات أو مراجعة أو حماية بيانات."]
    ],
    productsTitle: "أنظمة Dealix الأساسية",
    productsText:
      "نبدأ بأنظمة صغيرة قابلة للبيع والتسليم، ثم نوسعها إلى Operating System كامل للشركة.",
    products: [
      ["Revenue Command Room OS", "غرفة قيادة توضح الفرص، المتابعات، العروض، العملاء الساخنين، والقرار التالي."],
      ["WhatsApp / Inbox Follow-up OS", "نظام يصنف المحادثات، يجهز الردود، ويمنع ضياع المتابعات مع مراجعة بشرية."],
      ["Company Brain OS", "عقل تشغيلي يومي يقرأ الإيراد والعملاء والمخاطر ويقترح قرارات قابلة للتنفيذ."],
      ["AI Trust & Compliance OS", "سياسات، صلاحيات، human approval gates، وحماية بيانات لاستخدام AI بشكل آمن."]
    ],
    methodTitle: "منهجية تنفيذ لا تبيع وعودًا. تسلّم نظامًا.",
    method: [
      ["01", "Map", "نفهم نموذج العمل، مصادر الإيراد، القنوات، ومناطق التعطل."],
      ["02", "Design", "نحوّل المشكلة إلى workflow واضح، scope card، وacceptance criteria."],
      ["03", "Build", "نبني V0 سريع: ledger، dashboard، drafts، reports، وapproval gates."],
      ["04", "Operate", "نشغّل يوميًا: targets، follow-ups، proposals، command room، CEO report."],
      ["05", "Scale", "نوسّع بناءً على proof حقيقي، لا افتراضات."]
    ],
    comparisonTitle: "لماذا Dealix مختلفة؟",
    compare: [
      ["السوق العادي", "ما يقدمه غالبًا", "Dealix"],
      ["CRM", "تخزين بيانات وفرص", "طبقة تشغيل يومية تقول ماذا تفعل الآن."],
      ["Chatbot", "ردود آلية محدودة", "نظام متابعة وقرار وحوكمة، وليس مجرد رد."],
      ["Dashboard", "أرقام ورسوم", "غرفة قيادة تربط الرقم بالقرار والـnext action."],
      ["Agency", "حملات ومحتوى", "Revenue OS يربط الاستهداف، المتابعة، العروض، والردود."],
      ["Consulting", "توصيات ووثائق", "نظام يعمل، reports، proof، وتحسين مستمر."]
    ],
    pricingTitle: "باقات البداية",
    pricing: [
      ["AI Revenue Diagnostic", "مجاني", "20 دقيقة لفهم الوضع وتحديد 3 نقاط ضياع وفرصة بداية."],
      ["7-Day Command Room Sprint", "1,500–5,000 SAR", "Dashboard، lead ledger، follow-up queue، قوالب، وتقرير يومي."],
      ["30-Day AI Operating System", "8,000–25,000 SAR", "نظام تشغيل أوسع للإيراد، المتابعة، القرار، والثقة."]
    ],
    sectorsTitle: "القطاعات الأولى",
    sectors: ["العيادات", "العقار", "اللوجستيات", "التدريب", "وكالات التسويق", "B2B Services", "المقاولات", "معارض السيارات"],
    trustTitle: "Trust by design",
    trustText:
      "Dealix لا يبني AI عشوائي. كل إجراء خارجي حساس يحتاج مراجعة، وكل pain hypothesis، وكل target يحتاج source_url، ولا توجد وعود ROI وهمية.",
    finalTitle: "ابدأ بتشخيص واحد. لا تبنِ نظامًا ضخمًا قبل proof.",
    finalText:
      "أفضل بداية: 7-Day Company Diagnosis + Revenue Command Room. نحدد أين تضيع الفرص، نبني أول workflow، ونطلع أول قرارات تشغيلية."
  },
  en: {
    dir: "ltr",
    nav: ["Problem", "Systems", "Method", "Comparison", "Packages"],
    badge: "Company Brain + Revenue Command Room + Trust Gates",
    title: "Turn scattered sales and follow-up into a daily operating system.",
    lead:
      "Dealix builds AI operating systems for Saudi B2B companies — connecting revenue, follow-up, WhatsApp, proposals, reports, executive decisions, and governance into one measurable workflow.",
    primary: "Book a free diagnostic",
    secondary: "Explore systems",
    panelTitle: "Dealix Command Room",
    live: "Operationally ready",
    metrics: [
      ["100", "Companies researched daily", "Focused targeting"],
      ["25", "Drafts prepared", "Human review"],
      ["10", "Manual sends", "No random automation"],
      ["1", "Daily decision", "For leadership"]
    ],
    decision:
      "Today’s decision: focus one sector, review 25 opportunities, send only 10 messages, and push 3 diagnostic calls.",
    problemTitle: "Companies do not need more tools. They need an operating layer.",
    problemText:
      "Tools exist, but opportunities disappear across WhatsApp, email, teams, proposals, and reports. Dealix builds the operating layer above what already exists so leadership knows what happened and what to do today.",
    problems: [
      ["Lost opportunities", "Prospects ask, wait, and disappear because follow-up is not systemized."],
      ["WhatsApp outside measurement", "Important conversations lack classification, ownership, and next action."],
      ["Reports without decisions", "Plenty of numbers, but no clear daily executive decision."],
      ["AI without governance", "Teams use AI tools without policy, review, or data protection."]
    ],
    productsTitle: "Core Dealix systems",
    productsText:
      "We start with sellable, deliverable systems, then expand into a full company operating system.",
    products: [
      ["Revenue Command Room OS", "A command room for opportunities, follow-ups, proposals, hot leads, and next actions."],
      ["WhatsApp / Inbox Follow-up OS", "Classify conversations, draft replies, and prevent follow-up leakage with human review."],
      ["Company Brain OS", "A daily decision brain that reads revenue, customers, risks, and opportunities."],
      ["AI Trust & Compliance OS", "Policies, permissions, human approval gates, and data handling for responsible AI."]
    ],
    methodTitle: "A delivery method that ships systems, not promises.",
    method: [
      ["01", "Map", "Understand business model, revenue sources, channels, and bottlenecks."],
      ["02", "Design", "Turn the problem into a workflow, scope card, and acceptance criteria."],
      ["03", "Build", "Ship V0: ledger, dashboard, drafts, reports, and approval gates."],
      ["04", "Operate", "Run daily: targets, follow-ups, proposals, command room, and CEO report."],
      ["05", "Scale", "Expand based on proof, not assumptions."]
    ],
    comparisonTitle: "Why Dealix is different",
    compare: [
      ["Regular market", "Usually provides", "Dealix"],
      ["CRM", "Stores records and opportunities", "A daily operating layer that tells teams what to do now."],
      ["Chatbot", "Limited automated replies", "A follow-up, decision, and governance system."],
      ["Dashboard", "Charts and numbers", "A command room that connects data to next actions."],
      ["Agency", "Campaigns and content", "Revenue OS connecting targeting, follow-up, proposals, and replies."],
      ["Consulting", "Recommendations and documents", "Working system, reports, proof, and continuous improvement."]
    ],
    pricingTitle: "Starter packages",
    pricing: [
      ["AI Revenue Diagnostic", "Free", "20 minutes to identify 3 leakage points and the best starting workflow."],
      ["7-Day Command Room Sprint", "1,500–5,000 SAR", "Dashboard, lead ledger, follow-up queue, templates, and daily report."],
      ["30-Day AI Operating System", "8,000–25,000 SAR", "A wider operating system for revenue, follow-up, decisions, and trust."]
    ],
    sectorsTitle: "First target sectors",
    sectors: ["Clinics", "Real estate", "Logistics", "Training", "Marketing agencies", "B2B services", "Contracting", "Car showrooms"],
    trustTitle: "Trust by design",
    trustText:
      "Dealix does not build random AI. Every sensitive external action requires review, every pain is a hypothesis, every target needs a source URL, and fake ROI promises are blocked.",
    finalTitle: "Start with one diagnostic. Do not build a large system before proof.",
    finalText:
      "Best first move: 7-Day Company Diagnosis + Revenue Command Room. We identify leakage, build the first workflow, and produce the first operating decisions."
  }
} satisfies Record<Lang, any>;

function getLang(): Lang {
  const path = window.location.pathname.toLowerCase();
  if (path.startsWith("/en")) return "en";
  return "ar";
}

export function DealixWebsite() {
  const lang = getLang();
  const t = copy[lang];

  return (
    <main className={`page ${lang === "en" ? "ltr" : ""}`} dir={t.dir} lang={lang}>
      <nav className="nav">
        <div className="container navInner">
          <a className="logo" href={lang === "ar" ? "/ar" : "/en"} aria-label="Dealix">
            <span className="logoMark">D</span>
            <span>Dealix</span>
          </a>

          <div className="navLinks">
            {t.nav.map((item: string, index: number) => (
              <a key={item} href={`#s${index}`}>{item}</a>
            ))}
          </div>

          <div className="langSwitch">
            <a className={lang === "ar" ? "active" : ""} href="/ar">AR</a>
            <a className={lang === "en" ? "active" : ""} href="/en">EN</a>
          </div>
        </div>
      </nav>

      <section className="hero">
        <div className="container heroGrid">
          <div>
            <span className="badge"><span className="badgeDot" />{t.badge}</span>
            <h1><span className="gradientText">{t.title}</span></h1>
            <p className="lead">{t.lead}</p>
            <div className="ctaRow">
              <a className="btn btnPrimary" href="mailto:hello@dealix.me">{t.primary}</a>
              <a className="btn btnSecondary" href="#s1">{t.secondary}</a>
            </div>
          </div>

          <div className="osPanel">
            <div className="panelTop">
              <span>{t.panelTitle}</span>
              <span className="status">{t.live}</span>
            </div>

            <div className="metricGrid">
              {t.metrics.map((m: string[]) => (
                <div className="metricCard" key={m[1]}>
                  <div className="metricLabel">{m[1]}</div>
                  <div className="metricValue">{m[0]}</div>
                  <div className="metricNote">{m[2]}</div>
                </div>
              ))}
            </div>

            <div className="card decisionCard">
              <div className="metricLabel">Daily CEO Decision</div>
              <p>{t.decision}</p>
            </div>
          </div>
        </div>
      </section>

      <section id="s0" className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">The real problem</div>
            <h2>{t.problemTitle}</h2>
            <p className="sectionText">{t.problemText}</p>
          </div>
          <div className="grid4">
            {t.problems.map((p: string[]) => (
              <article className="card" key={p[0]}>
                <div className="icon" />
                <h3>{p[0]}</h3>
                <p>{p[1]}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="s1" className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">Operating systems</div>
            <h2>{t.productsTitle}</h2>
            <p className="sectionText">{t.productsText}</p>
          </div>
          <div className="grid4">
            {t.products.map((p: string[]) => (
              <article className="card" key={p[0]}>
                <div className="icon" />
                <h3>{p[0]}</h3>
                <p>{p[1]}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="s2" className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">Map → Design → Build → Operate → Scale</div>
            <h2>{t.methodTitle}</h2>
          </div>
          <div className="method">
            {t.method.map((s: string[]) => (
              <article className="step" key={s[1]}>
                <div className="stepNumber">{s[0]}</div>
                <h3>{s[1]}</h3>
                <p>{s[2]}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="s3" className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">Strategic comparison</div>
            <h2>{t.comparisonTitle}</h2>
          </div>

          <div className="compare">
            {t.compare.map((row: string[], index: number) => (
              <div className={`compareRow ${index === 0 ? "compareHead" : ""}`} key={row.join("-")}>
                {row.map((cell: string) => (
                  <div className="compareCell" key={cell}>
                    {index === 0 ? <strong>{cell}</strong> : cell}
                  </div>
                ))}
              </div>
            ))}
          </div>
        </div>
      </section>

      <section id="s4" className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">Commercial entry</div>
            <h2>{t.pricingTitle}</h2>
          </div>

          <div className="pricing">
            {t.pricing.map((p: string[], index: number) => (
              <article className={`priceCard ${index === 1 ? "featured" : ""}`} key={p[0]}>
                <h3>{p[0]}</h3>
                <div className="price">{p[1]}</div>
                <p>{p[2]}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="sectionHeader">
            <div className="eyebrow">Focus sectors</div>
            <h2>{t.sectorsTitle}</h2>
          </div>
          <div className="grid4">
            {t.sectors.map((sector: string) => (
              <div className="card" key={sector}>
                <h3>{sector}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container heroGrid">
          <div>
            <div className="eyebrow">Governance</div>
            <h2>{t.trustTitle}</h2>
            <p className="sectionText">{t.trustText}</p>
          </div>
          <div className="card">
            <h3>Approval Gates</h3>
            <ul>
              <li>Human review before sensitive external actions.</li>
              <li>Verified target and source URL required.</li>
              <li>No fake ROI or fabricated testimonials.</li>
              <li>Opt-out and suppression logic for outbound.</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="osPanel">
            <div className="sectionHeader">
              <div className="eyebrow">Founder-led GTM</div>
              <h2>{t.finalTitle}</h2>
              <p className="sectionText">{t.finalText}</p>
              <div className="ctaRow">
                <a className="btn btnPrimary" href="mailto:hello@dealix.me">{t.primary}</a>
                <a className="btn btnSecondary" href={lang === "ar" ? "/en" : "/ar"}>
                  {lang === "ar" ? "English version" : "النسخة العربية"}
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="container navInner">
          <div className="logo">
            <span className="logoMark">D</span>
            <span>Dealix</span>
          </div>
          <div>AI Operating Systems for Saudi B2B Companies</div>
        </div>
      </footer>
    </main>
  );
}
