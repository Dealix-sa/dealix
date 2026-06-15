// Onboarding step definitions. `schema` is an optional Zod-like validator
// ({ parse }) so the wizard can validate each step's data when present.

export interface SchemaLike {
  parse: (data: unknown) => unknown;
}

export interface OnboardingStep {
  id: string;
  title: string;
  titleEn: string;
  description: string;
  descriptionEn: string;
  isSkippable: boolean;
  schema?: SchemaLike;
}

export type OnboardingData = Record<string, Record<string, unknown>>;

export const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    id: "company",
    title: "معلومات الشركة",
    titleEn: "Company details",
    description: "أخبرنا عن شركتك حتى نخصّص النظام لك.",
    descriptionEn: "Tell us about your company so we can tailor the system.",
    isSkippable: false,
  },
  {
    id: "goals",
    title: "أهدافك",
    titleEn: "Your goals",
    description: "ما الذي تريد تحقيقه في أول 90 يوم؟",
    descriptionEn: "What do you want to achieve in the first 90 days?",
    isSkippable: true,
  },
  {
    id: "channels",
    title: "قنوات التواصل",
    titleEn: "Channels",
    description: "كيف تتواصل مع عملائك اليوم؟",
    descriptionEn: "How do you reach your customers today?",
    isSkippable: true,
  },
  {
    id: "review",
    title: "المراجعة",
    titleEn: "Review",
    description: "راجع بياناتك قبل البدء.",
    descriptionEn: "Review your details before you start.",
    isSkippable: false,
  },
];

export function getStepProgress(currentStep: number): number {
  if (ONBOARDING_STEPS.length === 0) return 0;
  const clamped = Math.min(Math.max(currentStep, 0), ONBOARDING_STEPS.length - 1);
  return Math.round(((clamped + 1) / ONBOARDING_STEPS.length) * 100);
}
