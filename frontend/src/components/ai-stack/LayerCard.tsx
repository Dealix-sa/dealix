/**
 * AI Stack Layer Card — single layer status with bilingual label + version.
 *
 * Renders one of the eleven canonical layers in a compact card. Hover state
 * surfaces the underlying module path so operators can dive into the code
 * with one click.
 */

import type { LayerHealth } from "@/lib/aiStackClient";

interface LayerCardProps {
  layer: LayerHealth;
  locale: "ar" | "en";
}

// Bilingual labels per layer for the demo UI.
const LAYER_LABELS_AR: Record<string, string> = {
  L1_source_passport: "جواز المصدر",
  L2_data_quality: "جودة البيانات",
  L3_intelligence: "الذكاء و RAG",
  L4_model_router: "موجّه النموذج",
  L5_agent_mesh: "شبكة الوكلاء",
  L6_governance: "بوابة الحوكمة",
  L7_proof_pack: "حزمة الإثبات",
  L8_value_ledger: "سجل القيمة",
  L9_capital_ledger: "سجل الرأسمال",
  L10_adoption: "التبني والاحتفاظ",
  L11_self_evolving: "التحسين الذاتي (وضع الظل)",
};

const LAYER_NUMBERS: Record<string, string> = {
  L1_source_passport: "L1",
  L2_data_quality: "L2",
  L3_intelligence: "L3",
  L4_model_router: "L4",
  L5_agent_mesh: "L5",
  L6_governance: "L6",
  L7_proof_pack: "L7",
  L8_value_ledger: "L8",
  L9_capital_ledger: "L9",
  L10_adoption: "L10",
  L11_self_evolving: "L11",
};

export function LayerCard({ layer, locale }: LayerCardProps) {
  const localizedLabel =
    locale === "ar"
      ? (LAYER_LABELS_AR[layer.layer] ?? layer.label)
      : layer.label;
  const statusColor = layer.healthy
    ? "border-emerald-500/40 bg-emerald-500/5"
    : "border-rose-500/40 bg-rose-500/5";
  const dotColor = layer.healthy ? "bg-emerald-500" : "bg-rose-500";

  return (
    <div
      className={`rounded-xl border ${statusColor} p-4 transition-all hover:scale-[1.01]`}
      data-layer={layer.layer}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <div className="flex items-center gap-2 text-xs font-mono text-muted-foreground">
            <span>{LAYER_NUMBERS[layer.layer] ?? layer.layer}</span>
            <span className="opacity-60">·</span>
            <span>v{layer.version}</span>
          </div>
          <h3 className="mt-1 text-base font-semibold text-foreground">
            {localizedLabel}
          </h3>
          {locale === "ar" ? (
            <p className="mt-0.5 text-xs text-muted-foreground">
              {layer.label}
            </p>
          ) : null}
        </div>
        <span
          className={`mt-1 inline-flex h-2.5 w-2.5 shrink-0 rounded-full ${dotColor}`}
          aria-label={layer.healthy ? "healthy" : "degraded"}
        />
      </div>
      <div className="mt-3 break-all font-mono text-[10px] leading-snug text-muted-foreground/80">
        {layer.module}
      </div>
      {!layer.healthy && layer.detail ? (
        <div className="mt-2 rounded-md bg-rose-500/10 px-2 py-1 text-xs text-rose-300">
          {layer.detail}
        </div>
      ) : null}
    </div>
  );
}
