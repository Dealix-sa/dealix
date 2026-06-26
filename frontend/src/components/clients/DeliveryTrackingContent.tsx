"use client";

import { useLocale } from "next-intl";
import { Package, Inbox } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

type DeliveryStage =
  | "intake"
  | "diagnosis"
  | "blueprint"
  | "build"
  | "qa"
  | "uat"
  | "launch"
  | "training"
  | "proof";

interface ClientProject {
  id: string;
  clientName: string;
  stage: DeliveryStage;
  owner: string;
}

const STAGE_LABEL_AR: Record<DeliveryStage, string> = {
  intake: "استيعاب",
  diagnosis: "تشخيص",
  blueprint: "مخطط",
  build: "بناء",
  qa: "ضمان الجودة",
  uat: "اختبار القبول",
  launch: "إطلاق",
  training: "تدريب",
  proof: "إثبات",
};

const STAGE_LABEL_EN: Record<DeliveryStage, string> = {
  intake: "Intake",
  diagnosis: "Diagnosis",
  blueprint: "Blueprint",
  build: "Build",
  qa: "QA",
  uat: "UAT",
  launch: "Launch",
  training: "Training",
  proof: "Proof",
};

const STAGE_ORDER: DeliveryStage[] = [
  "intake",
  "diagnosis",
  "blueprint",
  "build",
  "qa",
  "uat",
  "launch",
  "training",
  "proof",
];

// No fake client data — empty by default.
const PROJECTS: ClientProject[] = [];

export function DeliveryTrackingContent() {
  const locale = useLocale();
  const isAr = locale === "ar";

  const emptyTitle = isAr ? "لا يوجد عملاء بعد" : "No clients yet";
  const emptyHint = isAr
    ? "عندما تبدأ مشاريع العميل ستظهر هنا عبر تسع مراحل: استيعاب، تشخيص، مخطط، بناء، QA، UAT، إطلاق، تدريب، إثبات."
    : "When client projects start they'll appear here across nine stages: intake, diagnosis, blueprint, build, QA, UAT, launch, training, proof.";

  return (
    <div className="space-y-6">
      {/* Stages legend */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Package className="size-5 text-gold-400" />
            {isAr ? "مراحل التسليم" : "Delivery stages"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-2">
            {STAGE_ORDER.map((stage, idx) => (
              <Badge key={stage} variant="outline" className="gap-1">
                <span className="text-muted-foreground/60">{idx + 1}</span>
                {isAr ? STAGE_LABEL_AR[stage] : STAGE_LABEL_EN[stage]}
              </Badge>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Projects */}
      <Card>
        <CardHeader>
          <CardTitle>{isAr ? "مشاريع العميل" : "Client projects"}</CardTitle>
        </CardHeader>
        <CardContent>
          {PROJECTS.length === 0 ? (
            <div className="rounded-lg border border-dashed border-border p-10 text-center">
              <Inbox className="mx-auto size-10 text-muted-foreground/50 mb-3" />
              <p className="text-sm font-medium text-muted-foreground">{emptyTitle}</p>
              <p className="mt-1 text-xs text-muted-foreground/70 max-w-lg mx-auto">{emptyHint}</p>
            </div>
          ) : (
            <div className="space-y-3">
              {PROJECTS.map((p) => {
                const stageIdx = STAGE_ORDER.indexOf(p.stage);
                return (
                  <div key={p.id} className="rounded-lg border border-border p-4">
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{p.clientName}</span>
                      <Badge variant="gold">
                        {isAr ? STAGE_LABEL_AR[p.stage] : STAGE_LABEL_EN[p.stage]}
                      </Badge>
                    </div>
                    <p className="mt-1 text-xs text-muted-foreground">
                      {isAr ? `المسؤول: ${p.owner}` : `Owner: ${p.owner}`}
                    </p>
                    {/* Progress strip */}
                    <div className="mt-3 flex gap-1">
                      {STAGE_ORDER.map((s, i) => (
                        <div
                          key={s}
                          className={`h-1.5 flex-1 rounded-full ${
                            i <= stageIdx ? "bg-emerald-500/70" : "bg-border"
                          }`}
                          title={isAr ? STAGE_LABEL_AR[s] : STAGE_LABEL_EN[s]}
                        />
                      ))}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default DeliveryTrackingContent;