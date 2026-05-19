export type Lang = "ar" | "en";

export interface KpiItem {
  num: string;
  label: string;
  note?: string;
}

export interface CardItem {
  icon?: string;
  title: string;
  desc: string;
  stat?: string;
}

export interface FlowItem {
  icon: string;
  title: string;
  desc: string;
}

export interface StepItem {
  n: string;
  title: string;
  desc: string;
}

export interface BarItem {
  label: string;
  before: string;
  after: string;
  beforePct: number;
  afterPct: number;
  lowerBetter?: boolean;
}

export interface RoiCol {
  label: string;
  value: string;
  pct: number;
  tone: "danger" | "ok";
  items: string[];
}

export interface RoiDelta {
  label: string;
  value: string;
}

export interface GateItem {
  code: string;
  label: string;
}

export interface PriceItem {
  tier: string;
  name: string;
  price: string;
  period: string;
  items: string[];
  badge?: string;
  featured?: boolean;
}

export interface CtaButton {
  label: string;
  href: string;
  primary: boolean;
}

export type Block =
  | { type: "kpis"; items: KpiItem[] }
  | { type: "cards"; tone?: "danger"; items: CardItem[] }
  | { type: "flow"; items: FlowItem[] }
  | { type: "steps"; items: StepItem[] }
  | { type: "table"; head: string[]; highlight: number; rows: string[][] }
  | { type: "bars"; items: BarItem[] }
  | { type: "roi"; unit: string; cols: RoiCol[]; delta?: RoiDelta }
  | { type: "gates"; items: GateItem[] }
  | { type: "pricing"; items: PriceItem[] }
  | { type: "bullets"; title?: string; items: string[] }
  | { type: "note"; text: string };

export interface SlideContent {
  kicker?: string;
  title: string;
  headline?: string;
  subtitle?: string;
  meta?: string;
  tags?: string[];
  eyebrow?: string;
  blocks?: Block[];
  buttons?: CtaButton[];
  contact?: string;
}

export interface Slide {
  id: string;
  layout: "cover" | "standard" | "cta";
  ar: SlideContent;
  en: SlideContent;
}

export interface PitchContent {
  meta: Record<string, string>;
  ui: Record<Lang, Record<string, string>>;
  slides: Slide[];
}
