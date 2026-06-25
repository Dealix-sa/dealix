export type SectorKey = "clinics" | "real_estate" | "logistics" | "training_centers" | "marketing_agencies" | "b2b_services";

interface SectorProfile {
  buyer: string;
  painSignals: string[];
  bestOffer: string;
  discoveryQuestions: string[];
}

export const sectorProfiles: Record<SectorKey, SectorProfile> = {
  clinics: {
    buyer: "Clinic owner or operations manager",
    painSignals: ["missed appointment follow-ups", "WhatsApp conversations without owner", "manual booking reminders"],
    bestOffer: "Follow-up Recovery OS",
    discoveryQuestions: [
      "How many booking inquiries arrive daily?",
      "Who owns follow-up after the first reply?",
      "Do you track delayed patient conversations?",
    ],
  },
  real_estate: {
    buyer: "Brokerage owner or sales manager",
    painSignals: ["leads disappear after first inquiry", "follow-up is inconsistent", "open offers are not reviewed daily"],
    bestOffer: "Revenue Command Room OS",
    discoveryQuestions: [
      "How do you know which inquiry is hot today?",
      "How many inquiries are followed up after three days?",
      "Who reviews stale opportunities?",
    ],
  },
  logistics: {
    buyer: "Commercial director or founder",
    painSignals: ["B2B proposals need structured follow-up", "account ownership is unclear", "sales cycle is long"],
    bestOffer: "Revenue Command Room OS",
    discoveryQuestions: [
      "How many open proposals do you have this month?",
      "Who owns the next action for each account?",
      "How do you escalate stuck proposals?",
    ],
  },
  training_centers: {
    buyer: "Center owner or admissions manager",
    painSignals: ["registration follow-up is manual", "cohort pipeline is unclear", "late responses reduce conversion"],
    bestOffer: "Follow-up Recovery OS",
    discoveryQuestions: [
      "How many course inquiries arrive weekly?",
      "Who follows up before cohort start dates?",
      "Do you track reasons for lost registrations?",
    ],
  },
  marketing_agencies: {
    buyer: "Agency owner or account director",
    painSignals: ["client reporting is manual", "delivery proof is scattered", "renewal conversations are late"],
    bestOffer: "Client Delivery OS",
    discoveryQuestions: [
      "How do clients see what was delivered this week?",
      "Where are acceptance criteria stored?",
      "How do you prepare renewal proof?",
    ],
  },
  b2b_services: {
    buyer: "Founder or general manager",
    painSignals: ["pipeline is in memory or spreadsheets", "follow-up depends on individuals", "proposals lack next actions"],
    bestOffer: "Revenue Command Room OS",
    discoveryQuestions: [
      "Where do new opportunities live today?",
      "How do you review open proposals?",
      "What does the team check every morning?",
    ],
  },
};

export function normalizeSector(input: string | undefined): SectorKey {
  const key = (input || "b2b_services").trim().toLowerCase().replace(/\s+/g, "_").replace(/-/g, "_");
  if (key in sectorProfiles) return key as SectorKey;
  return "b2b_services";
}

export function buildSalesAgentDraft(input: {
  company: string;
  sector?: string;
  city?: string;
  sourceUrl?: string;
  senderIdentity?: string;
}) {
  const sector = normalizeSector(input.sector);
  const profile = sectorProfiles[sector];
  const company = input.company?.trim() || "Target Company";
  const senderIdentity = input.senderIdentity?.trim() || "Dealix Sales Assistant";
  const sourceUrl = input.sourceUrl?.trim() || "manual_review_required";
  const city = input.city?.trim() || "Saudi Arabia";
  const primaryPain = profile.painSignals[0];

  return {
    mode: "draft_only",
    requiresApproval: true,
    externalSendEnabled: false,
    company,
    sector,
    city,
    sourceUrl,
    senderIdentity,
    buyer: profile.buyer,
    painHypothesis: primaryPain,
    recommendedOffer: profile.bestOffer,
    discoveryQuestions: profile.discoveryQuestions,
    draftAr: `السلام عليكم، أنا من ${senderIdentity}.\n\nنساعد شركات مثل ${company} على تحويل المتابعة والعروض والفرص اليومية إلى نظام تشغيل واضح: من يحتاج متابعة اليوم؟ ما الفرص الساخنة؟ وما القرار التجاري الأهم؟\n\nبناء على طبيعة قطاعكم، قد يكون أفضل مدخل هو ${profile.bestOffer}. هذه مجرد فرضية أولية مبنية على القطاع وليست ادعاء عن وضعكم. نبدأ عادة بتشخيص صغير يوضح أين تضيع المتابعة أو القرار، ثم sprint قصير بمخرجات قابلة للمراجعة.\n\nإذا مناسب، أرسل لكم صفحة واحدة مخصصة قبل أي اجتماع.\n\nلإيقاف التواصل، أرسل إيقاف.`,
    negotiationGuardrails: [
      "Start with diagnostic or 7-day sprint.",
      "Do not discount without reducing scope.",
      "Offer proof pack instead of guaranteed revenue.",
      "Keep first scope to one pain and one channel.",
      "Require owner approval before external use.",
    ],
  };
}
