import type { Band, NextStep, ToolQuestion } from "@/lib/wave3/scoring";

export interface BandRecommendation {
  osAr: string;
  osEn: string;
  nextStep: NextStep;
}

export interface QuizToolDef {
  slug: string;
  kind: "quiz";
  titleAr: string;
  titleEn: string;
  introAr: string;
  introEn: string;
  questions: ToolQuestion[];
  recommended: Record<Band, BandRecommendation>;
  disclaimer: "default" | "educational";
}

export interface LeakageToolDef {
  slug: string;
  kind: "leakage";
  titleAr: string;
  titleEn: string;
  introAr: string;
  introEn: string;
  recommended: Record<Band, BandRecommendation>;
  disclaimer: "educational";
}

export type ToolDef = QuizToolDef | LeakageToolDef;
