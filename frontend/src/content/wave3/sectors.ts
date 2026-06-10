export type Sector = {
  slug: string;
  nameAr: string;
  nameEn: string;
  descAr: string;
  descEn: string;
  painAr: string[];
  painEn: string[];
  outcomesAr: string[];
  outcomesEn: string[];
  recommendedOsAr: string;
  recommendedOsEn: string;
};

export const SECTORS: Sector[] = [
  {
    slug: "real-estate",
    nameAr: "العقار",
    nameEn: "Real Estate",
    descAr: "مكاتب ومطوّرون عقاريون لديهم فرص كثيرة لكن المتابعة والإثبات غير منظمين.",
    descEn: "Brokerages and developers with many opportunities but disorganized follow-up and proof.",
    painAr: ["فرص تتسرّب بلا متابعة موثّقة", "لا وضوح في مالك كل فرصة", "صعوبة إثبات ما تم للإدارة"],
    painEn: ["Opportunities leak without documented follow-up", "No clear owner per opportunity", "Hard to prove activity to leadership"],
    outcomesAr: ["خريطة فرص واضحة", "سجل إثبات لكل قرار", "لوحة الخطوة التالية"],
    outcomesEn: ["A clear opportunity map", "A proof register per decision", "A next-action board"],
    recommendedOsAr: "Command Sprint",
    recommendedOsEn: "Command Sprint",
  },
  {
    slug: "clinics",
    nameAr: "العيادات والرعاية",
    nameEn: "Clinics & Healthcare",
    descAr: "عيادات لديها استفسارات يومية لكن المتابعة والموافقات غير محكومة.",
    descEn: "Clinics with daily inquiries but ungoverned follow-up and approvals.",
    painAr: ["استفسارات بلا رد منظّم", "لا سجل لما تم", "حساسية الخصوصية"],
    painEn: ["Inquiries with no organized reply", "No record of what happened", "Privacy sensitivity"],
    outcomesAr: ["متابعة موثّقة بموافقة بشرية", "سجل إثبات محكوم", "احترام الخصوصية"],
    outcomesEn: ["Documented follow-up with human approval", "A governed proof register", "Privacy respected"],
    recommendedOsAr: "Command Sprint",
    recommendedOsEn: "Command Sprint",
  },
  {
    slug: "professional-services",
    nameAr: "الخدمات المهنية",
    nameEn: "Professional Services",
    descAr: "وكالات واستشارات تحتاج تثبت قيمتها لعملائها بإثبات منظم.",
    descEn: "Agencies and consultancies that need to prove their value with structured proof.",
    painAr: ["العميل يطلب إثباتاً أسبوعياً", "العروض تأخذ وقتاً", "لا صورة قرار موحّدة"],
    painEn: ["Clients ask for weekly proof", "Proposals take too long", "No unified decision picture"],
    outcomesAr: ["Proof Pack جاهز للعميل", "قالب عروض أسرع", "ملخص تنفيذي واضح"],
    outcomesEn: ["A client-ready Proof Pack", "A faster proposal template", "A clear executive brief"],
    recommendedOsAr: "Command Sprint",
    recommendedOsEn: "Command Sprint",
  },
  {
    slug: "retail-ecommerce",
    nameAr: "التجزئة والتجارة الإلكترونية",
    nameEn: "Retail & E-commerce",
    descAr: "متاجر لديها استفسارات وسلال متروكة تحتاج متابعة منظمة وآمنة.",
    descEn: "Stores with inquiries and abandoned carts needing organized, safe follow-up.",
    painAr: ["استفسارات كثيرة بلا أولوية", "متابعة يدوية مشتتة", "لا قياس لما ينجح"],
    painEn: ["Many inquiries with no priority", "Scattered manual follow-up", "No measure of what works"],
    outcomesAr: ["ترتيب الفرص بالأولوية", "مسودات رد قابلة للمراجعة", "لوحة خطوات تالية"],
    outcomesEn: ["Prioritized opportunities", "Review-ready reply drafts", "A next-action board"],
    recommendedOsAr: "Command Sprint",
    recommendedOsEn: "Command Sprint",
  },
  {
    slug: "contracting",
    nameAr: "المقاولات",
    nameEn: "Contracting",
    descAr: "شركات مقاولات لديها عطاءات وفرص تحتاج وضوحاً في القرار التنفيذي القادم.",
    descEn: "Contractors with bids and opportunities needing clarity on the next executive decision.",
    painAr: ["عطاءات بلا متابعة موثّقة", "قرارات تتأخر", "لا صورة تنفيذية موحّدة"],
    painEn: ["Bids without documented follow-up", "Delayed decisions", "No unified executive picture"],
    outcomesAr: ["خريطة فرص العطاءات", "سجل موافقات", "ملخص تنفيذي للقرار"],
    outcomesEn: ["A bid-opportunity map", "An approval register", "An executive decision brief"],
    recommendedOsAr: "Command Sprint",
    recommendedOsEn: "Command Sprint",
  },
];

export function sectorSlugs(): string[] {
  return SECTORS.map((s) => s.slug);
}

export function getSector(slug: string): Sector | undefined {
  return SECTORS.find((s) => s.slug === slug);
}
