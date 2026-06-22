import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import {
  Activity,
  AlertTriangle,
  Brain,
  Lightbulb,
  ShieldCheck,
  Target,
  Zap,
} from "lucide-react";

type SignalType =
  | "revenue"
  | "pain"
  | "opportunity"
  | "risk"
  | "market"
  | "competitor"
  | "bottleneck";

type Effort = "low" | "medium" | "high";

const signalTypeOptions: SignalType[] = [
  "revenue",
  "pain",
  "opportunity",
  "risk",
  "market",
  "competitor",
  "bottleneck",
];

export default function BrainOS() {
  const utils = trpc.useUtils();
  const stats = trpc.brain.dashboardStats.useQuery();
  const signals = trpc.brain.signalList.useQuery();
  const decisions = trpc.brain.decisionList.useQuery();
  const risks = trpc.brain.riskList.useQuery();
  const opportunities = trpc.brain.opportunityList.useQuery();

  const createSignal = trpc.brain.signalCreate.useMutation({
    onSuccess: () => {
      utils.brain.signalList.invalidate();
      utils.brain.dashboardStats.invalidate();
    },
  });

  const createDecision = trpc.brain.decisionCreate.useMutation({
    onSuccess: () => {
      utils.brain.decisionList.invalidate();
      utils.brain.dashboardStats.invalidate();
    },
  });

  const createRisk = trpc.brain.riskCreate.useMutation({
    onSuccess: () => {
      utils.brain.riskList.invalidate();
      utils.brain.dashboardStats.invalidate();
    },
  });

  const createOpportunity = trpc.brain.opportunityCreate.useMutation({
    onSuccess: () => {
      utils.brain.opportunityList.invalidate();
      utils.brain.dashboardStats.invalidate();
    },
  });

  const [newSignal, setNewSignal] = useState({
    signalType: "revenue" as SignalType,
    source: "",
    description: "",
    strength: 5,
    confidence: 0.5,
  });

  const [newDecision, setNewDecision] = useState({
    decision: "",
    owner: "",
    nextAction: "",
    metric: "",
    assumption: "",
    priority: 5,
  });

  const [newRisk, setNewRisk] = useState({
    risk: "",
    probability: 3,
    impact: 3,
    mitigation: "",
    owner: "",
  });

  const [newOpportunity, setNewOpportunity] = useState({
    opportunity: "",
    potentialValue: "0",
    confidence: 0.5,
    effort: "medium" as Effort,
    owner: "",
  });

  const signalBadge = (type: string) => {
    const map: Record<string, string> = {
      revenue: "bg-emerald-100 text-emerald-700",
      pain: "bg-red-100 text-red-700",
      opportunity: "bg-amber-100 text-amber-700",
      risk: "bg-orange-100 text-orange-700",
      bottleneck: "bg-slate-100 text-slate-700",
      market: "bg-blue-100 text-blue-700",
      competitor: "bg-purple-100 text-purple-700",
    };

    return map[type] || "bg-gray-100 text-gray-700";
  };

  const priorityColor = (priority: number) => {
    if (priority >= 8) return "bg-red-100 text-red-700";
    if (priority >= 6) return "bg-amber-100 text-amber-700";
    if (priority >= 4) return "bg-blue-100 text-blue-700";
    return "bg-slate-100 text-slate-700";
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8] p-6" dir="rtl">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-[#15807A]">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-[#0A1F1E]">
                Company Brain OS
              </h1>
              <p className="text-sm text-[#4A6B69]">
                نظام القرار اليومي: signals، decisions، risks، opportunities،
                وdiscipline واضح للمتابعة.
              </p>
            </div>
          </div>

          <Badge variant="outline" className="border-[#15807A] text-[#15807A]">
            <ShieldCheck className="ml-1 h-3 w-3" />
            Governed and reviewable
          </Badge>
        </div>

        <div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-5">
          {[
            { icon: Activity, label: "Signals", value: stats.data?.signals ?? 0 },
            {
              icon: Target,
              label: "Decisions",
              value: stats.data?.decisions ?? 0,
            },
            {
              icon: AlertTriangle,
              label: "Active Risks",
              value: stats.data?.activeRisks ?? 0,
            },
            {
              icon: Lightbulb,
              label: "Opportunities",
              value: stats.data?.opportunities ?? 0,
            },
            {
              icon: Zap,
              label: "Experiments",
              value: stats.data?.experiments ?? 0,
            },
          ].map((item) => (
            <Card key={item.label} className="border-[#E8F4F3] bg-white">
              <CardContent className="flex items-center gap-3 p-4">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-[#E8F4F3]">
                  <item.icon className="h-5 w-5 text-[#15807A]" />
                </div>
                <div>
                  <p className="text-xs text-[#4A6B69]">{item.label}</p>
                  <p className="text-xl font-bold text-[#0A1F1E]">
                    {item.value}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid gap-8 lg:grid-cols-3">
          <div className="space-y-6">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <Activity className="h-4 w-4 text-[#15807A]" />
                  Signals Feed
                </CardTitle>
                <CardDescription>
                  ما الذي نراه الآن في السوق، الإيراد، أو داخل الشركة؟
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {signals.data?.slice(0, 6).map((signal) => (
                  <div key={signal.id} className="rounded-xl bg-[#F0F9F8] p-3">
                    <Badge
                      className={`${signalBadge(
                        signal.signalType,
                      )} mb-2 border-0 text-[10px]`}
                    >
                      {signal.signalType}
                    </Badge>
                    <p className="text-sm text-[#0A1F1E]">
                      {signal.description}
                    </p>
                    <p className="mt-1 text-xs text-[#8CB3B0]">
                      {signal.source || "auto"} • strength{" "}
                      {Math.round(signal.strength)}/10 • confidence{" "}
                      {(Number(signal.confidence ?? 0.5) * 100).toFixed(0)}%
                    </p>
                  </div>
                ))}

                <div className="space-y-3 border-t border-[#E8F4F3] pt-4">
                  <Select
                    value={newSignal.signalType}
                    onValueChange={(value) =>
                      setNewSignal({
                        ...newSignal,
                        signalType: value as SignalType,
                      })
                    }
                  >
                    <SelectTrigger className="border-[#E8F4F3]">
                      <SelectValue placeholder="نوع الإشارة" />
                    </SelectTrigger>
                    <SelectContent>
                      {signalTypeOptions.map((type) => (
                        <SelectItem key={type} value={type}>
                          {type}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>

                  <Textarea
                    placeholder="وصف الإشارة"
                    className="border-[#E8F4F3]"
                    value={newSignal.description}
                    onChange={(event) =>
                      setNewSignal({
                        ...newSignal,
                        description: event.target.value,
                      })
                    }
                  />

                  <Input
                    placeholder="المصدر"
                    className="border-[#E8F4F3]"
                    value={newSignal.source}
                    onChange={(event) =>
                      setNewSignal({ ...newSignal, source: event.target.value })
                    }
                  />

                  <div className="flex gap-2">
                    <Input
                      type="number"
                      className="border-[#E8F4F3]"
                      value={newSignal.strength}
                      onChange={(event) =>
                        setNewSignal({
                          ...newSignal,
                          strength: parseInt(event.target.value || "5", 10),
                        })
                      }
                    />
                    <Button
                      className="bg-[#15807A] hover:bg-[#0F5F5A]"
                      onClick={() => createSignal.mutate(newSignal)}
                    >
                      Add signal
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <Target className="h-4 w-4 text-[#15807A]" />
                  Decisions Log
                </CardTitle>
                <CardDescription>
                  كل قرار يجب أن يملك owner وmetric وnext action.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {decisions.data?.slice(0, 6).map((decision) => (
                  <div key={decision.id} className="rounded-xl bg-[#F0F9F8] p-3">
                    <div className="mb-2 flex items-center justify-between">
                      <Badge
                        className={`${priorityColor(
                          decision.priority,
                        )} border-0 text-[10px]`}
                      >
                        P{decision.priority}
                      </Badge>
                      <span className="text-xs text-[#8CB3B0]">
                        {decision.owner}
                      </span>
                    </div>
                    <p className="text-sm text-[#0A1F1E]">
                      {decision.decision}
                    </p>
                    <p className="mt-1 text-xs text-[#4A6B69]">
                      Next: {decision.nextAction}
                    </p>
                    {decision.metric && (
                      <p className="text-xs text-[#8CB3B0]">
                        Metric: {decision.metric}
                      </p>
                    )}
                  </div>
                ))}

                <div className="space-y-3 border-t border-[#E8F4F3] pt-4">
                  <Textarea
                    placeholder="القرار"
                    className="border-[#E8F4F3]"
                    value={newDecision.decision}
                    onChange={(event) =>
                      setNewDecision({
                        ...newDecision,
                        decision: event.target.value,
                      })
                    }
                  />

                  <Input
                    placeholder="Owner"
                    className="border-[#E8F4F3]"
                    value={newDecision.owner}
                    onChange={(event) =>
                      setNewDecision({
                        ...newDecision,
                        owner: event.target.value,
                      })
                    }
                  />

                  <Input
                    placeholder="Next Action"
                    className="border-[#E8F4F3]"
                    value={newDecision.nextAction}
                    onChange={(event) =>
                      setNewDecision({
                        ...newDecision,
                        nextAction: event.target.value,
                      })
                    }
                  />

                  <div className="flex gap-2">
                    <Input
                      placeholder="Metric"
                      className="border-[#E8F4F3]"
                      value={newDecision.metric}
                      onChange={(event) =>
                        setNewDecision({
                          ...newDecision,
                          metric: event.target.value,
                        })
                      }
                    />
                    <Input
                      type="number"
                      className="w-28 border-[#E8F4F3]"
                      value={newDecision.priority}
                      onChange={(event) =>
                        setNewDecision({
                          ...newDecision,
                          priority: parseInt(event.target.value || "5", 10),
                        })
                      }
                    />
                  </div>

                  <Button
                    className="bg-[#15807A] hover:bg-[#0F5F5A]"
                    onClick={() =>
                      createDecision.mutate({
                        ...newDecision,
                        status: "pending",
                      })
                    }
                  >
                    Add decision
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <AlertTriangle className="h-4 w-4 text-[#c0392b]" />
                  Risk Register
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {risks.data?.slice(0, 5).map((risk) => (
                  <div key={risk.id} className="rounded-xl bg-[#F0F9F8] p-3">
                    <div className="mb-1 flex items-center justify-between">
                      <span className="text-xs font-medium text-[#c0392b]">
                        Severity {risk.severity}
                      </span>
                      <span className="text-xs text-[#8CB3B0]">
                        {risk.owner || "Unassigned"}
                      </span>
                    </div>
                    <p className="text-sm text-[#0A1F1E]">{risk.risk}</p>
                    {risk.mitigation && (
                      <p className="mt-1 text-xs text-green-700">
                        Mitigation: {risk.mitigation}
                      </p>
                    )}
                  </div>
                ))}

                <div className="space-y-3 border-t border-[#E8F4F3] pt-4">
                  <Textarea
                    placeholder="المخاطرة"
                    className="border-[#E8F4F3]"
                    value={newRisk.risk}
                    onChange={(event) =>
                      setNewRisk({ ...newRisk, risk: event.target.value })
                    }
                  />
                  <Input
                    placeholder="Mitigation"
                    className="border-[#E8F4F3]"
                    value={newRisk.mitigation}
                    onChange={(event) =>
                      setNewRisk({
                        ...newRisk,
                        mitigation: event.target.value,
                      })
                    }
                  />
                  <div className="flex gap-2">
                    <Input
                      type="number"
                      className="border-[#E8F4F3]"
                      value={newRisk.probability}
                      onChange={(event) =>
                        setNewRisk({
                          ...newRisk,
                          probability: parseInt(event.target.value || "3", 10),
                        })
                      }
                    />
                    <Input
                      type="number"
                      className="border-[#E8F4F3]"
                      value={newRisk.impact}
                      onChange={(event) =>
                        setNewRisk({
                          ...newRisk,
                          impact: parseInt(event.target.value || "3", 10),
                        })
                      }
                    />
                  </div>
                  <Button
                    className="bg-[#c0392b] hover:bg-[#a93226]"
                    onClick={() => createRisk.mutate(newRisk)}
                  >
                    Add risk
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>

          <div className="space-y-6">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-[#0A1F1E]">
                  <Lightbulb className="h-4 w-4 text-[#15807A]" />
                  Opportunity Register
                </CardTitle>
                <CardDescription>
                  فرص قابلة للتنفيذ، مع potential value وeffort واضحين.
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                {opportunities.data?.slice(0, 6).map((opportunity) => (
                  <div
                    key={opportunity.id}
                    className="rounded-xl bg-[#F0F9F8] p-3"
                  >
                    <div className="mb-1 flex items-center justify-between">
                      <Badge
                        className={`${priorityColor(
                          opportunity.priority,
                        )} border-0 text-[10px]`}
                      >
                        P{opportunity.priority}
                      </Badge>
                      <span className="text-xs text-[#8CB3B0]">
                        {opportunity.effort} effort
                      </span>
                    </div>
                    <p className="text-sm text-[#0A1F1E]">
                      {opportunity.opportunity}
                    </p>
                    <p className="mt-1 text-xs text-[#4A6B69]">
                      {opportunity.potentialValue} SAR •{" "}
                      {(Number(opportunity.confidence ?? 0.5) * 100).toFixed(0)}%
                      {" "}confidence
                    </p>
                    {opportunity.owner && (
                      <p className="text-xs text-[#8CB3B0]">
                        Owner: {opportunity.owner}
                      </p>
                    )}
                  </div>
                ))}

                <div className="space-y-3 border-t border-[#E8F4F3] pt-4">
                  <Textarea
                    placeholder="الفرصة"
                    className="border-[#E8F4F3]"
                    value={newOpportunity.opportunity}
                    onChange={(event) =>
                      setNewOpportunity({
                        ...newOpportunity,
                        opportunity: event.target.value,
                      })
                    }
                  />

                  <div className="flex gap-2">
                    <Input
                      placeholder="Potential Value (SAR)"
                      className="border-[#E8F4F3]"
                      value={newOpportunity.potentialValue}
                      onChange={(event) =>
                        setNewOpportunity({
                          ...newOpportunity,
                          potentialValue: event.target.value,
                        })
                      }
                    />
                    <Input
                      type="number"
                      className="w-28 border-[#E8F4F3]"
                      value={newOpportunity.confidence}
                      onChange={(event) =>
                        setNewOpportunity({
                          ...newOpportunity,
                          confidence: Number(event.target.value),
                        })
                      }
                    />
                  </div>

                  <Select
                    value={newOpportunity.effort}
                    onValueChange={(value) =>
                      setNewOpportunity({
                        ...newOpportunity,
                        effort: value as Effort,
                      })
                    }
                  >
                    <SelectTrigger className="border-[#E8F4F3]">
                      <SelectValue placeholder="Effort" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low</SelectItem>
                      <SelectItem value="medium">Medium</SelectItem>
                      <SelectItem value="high">High</SelectItem>
                    </SelectContent>
                  </Select>

                  <Button
                    className="bg-[#15807A] hover:bg-[#0F5F5A]"
                    onClick={() => createOpportunity.mutate(newOpportunity)}
                  >
                    Add opportunity
                  </Button>
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#0A1F1E] bg-[#0A1F1E] text-white">
              <CardContent className="p-5">
                <p className="text-sm font-semibold">Decision Discipline</p>
                <ul className="mt-3 space-y-2 text-xs text-[#B7D2D0]">
                  <li>• كل قرار يجب أن يملك owner.</li>
                  <li>• كل قرار يجب أن يملك metric أو signal يبرره.</li>
                  <li>• كل مخاطرة يجب أن تملك mitigation أو next review.</li>
                  <li>• كل فرصة يجب أن ترتبط بقيمة وجهد زمني واضح.</li>
                </ul>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}