"use client";

import { useLocale } from "next-intl";
import {
  ShieldAlert,
  ShieldCheck,
  Mail,
  MessageCircle,
  Smartphone,
  Lock,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface EnvFlag {
  key: string;
  labelAr: string;
  labelEn: string;
  defaultValue: boolean;
  descriptionAr: string;
  descriptionEn: string;
}

const ENV_FLAGS: EnvFlag[] = [
  {
    key: "OUTBOUND_MODE",
    labelAr: "OUTBOUND_MODE",
    labelEn: "OUTBOUND_MODE",
    defaultValue: false,
    descriptionAr: "draft_only افتراضياً — لا إرسال خارجي حي.",
    descriptionEn: "draft_only by default — no live outbound send.",
  },
  {
    key: "ENABLE_LIVE_EMAIL_SEND",
    labelAr: "ENABLE_LIVE_EMAIL_SEND",
    labelEn: "ENABLE_LIVE_EMAIL_SEND",
    defaultValue: false,
    descriptionAr: "إرسال إيميل حي معطّل افتراضياً.",
    descriptionEn: "Live email send disabled by default.",
  },
  {
    key: "ENABLE_LIVE_WHATSAPP_SEND",
    labelAr: "ENABLE_LIVE_WHATSAPP_SEND",
    labelEn: "ENABLE_LIVE_WHATSAPP_SEND",
    defaultValue: false,
    descriptionAr: "إرسال واتساب حي معطّل افتراضياً.",
    descriptionEn: "Live WhatsApp send disabled by default.",
  },
  {
    key: "ENABLE_LIVE_SMS_SEND",
    labelAr: "ENABLE_LIVE_SMS_SEND",
    labelEn: "ENABLE_LIVE_SMS_SEND",
    defaultValue: false,
    descriptionAr: "إرسال SMS حي معطّل افتراضياً.",
    descriptionEn: "Live SMS send disabled by default.",
  },
  {
    key: "REQUIRE_HUMAN_APPROVAL",
    labelAr: "REQUIRE_HUMAN_APPROVAL",
    labelEn: "REQUIRE_HUMAN_APPROVAL",
    defaultValue: true,
    descriptionAr: "موافقة بشرية إلزامية قبل أي إرسال أو إجراء خارجي.",
    descriptionEn: "Mandatory human approval before any external send or action.",
  },
  {
    key: "ENFORCE_SAFETY_GATES",
    labelAr: "ENFORCE_SAFETY_GATES",
    labelEn: "ENFORCE_SAFETY_GATES",
    defaultValue: true,
    descriptionAr: "بوابات الأمان لكل قناة مطبّقة قبل الإرسال.",
    descriptionEn: "Per-channel safety gates enforced before send.",
  },
];

interface ChannelChecklist {
  channel: "email" | "whatsapp" | "sms";
  labelAr: string;
  labelEn: string;
  icon: React.ComponentType<{ className?: string }>;
  items: { key: string; labelAr: string; labelEn: string; descriptionAr: string; descriptionEn: string }[];
}

const CHANNEL_CHECKLISTS: ChannelChecklist[] = [
  {
    channel: "email",
    labelAr: "جاهزية الإيميل",
    labelEn: "Email readiness",
    icon: Mail,
    items: [
      {
        key: "spf",
        labelAr: "SPF",
        labelEn: "SPF",
        descriptionAr: "سجل SPF يحدد الخوادم المخوّلة لإرسال البريد لنطاقك.",
        descriptionEn: "SPF record authorizes servers allowed to send mail for your domain.",
      },
      {
        key: "dkim",
        labelAr: "DKIM",
        labelEn: "DKIM",
        descriptionAr: "توقيع DKIM يتحقق من سلامة البريد ومنع التزوير.",
        descriptionEn: "DKIM signature verifies email integrity and prevents spoofing.",
      },
      {
        key: "dmarc",
        labelAr: "DMARC",
        labelEn: "DMARC",
        descriptionAr: "سياسة DMARC تحدد التعامل مع البريد الذي يفشل SPF/DKIM.",
        descriptionEn: "DMARC policy dictates handling of mail failing SPF/DKIM.",
      },
    ],
  },
  {
    channel: "whatsapp",
    labelAr: "جاهزية واتساب",
    labelEn: "WhatsApp readiness",
    icon: MessageCircle,
    items: [
      {
        key: "optin",
        labelAr: "موافقة العميل (opt-in)",
        labelEn: "Customer opt-in",
        descriptionAr: "موافقة صريحة من العميل لاستقبال رسائل واتساب.",
        descriptionEn: "Explicit consent from the customer to receive WhatsApp messages.",
      },
      {
        key: "template",
        labelAr: "قالب معتمد",
        labelEn: "Approved template",
        descriptionAr: "استخدام قالب واتساب معتمد خارج نافذة ٢٤ ساعة.",
        descriptionEn: "Use an approved WhatsApp template outside the 24h window.",
      },
      {
        key: "window24h",
        labelAr: "نافذة ٢٤ ساعة",
        labelEn: "24h window",
        descriptionAr: "الالتزام بنافذة ٢٤ ساعة بعد رسالة العميل للرسائل الحرة.",
        descriptionEn: "Respect the 24h window after a customer message for free-form messages.",
      },
    ],
  },
  {
    channel: "sms",
    labelAr: "جاهزية SMS",
    labelEn: "SMS readiness",
    icon: Smartphone,
    items: [
      {
        key: "consent",
        labelAr: "موافقة صريحة",
        labelEn: "Explicit consent",
        descriptionAr: "موافقة العميل على استقبال SMS قبل أي إرسال.",
        descriptionEn: "Customer consent to receive SMS before any send.",
      },
      {
        key: "stop",
        labelAr: "آلية STOP",
        labelEn: "STOP mechanism",
        descriptionAr: "إمكانية إيقاف الرسائل بكلمة STOP والمعالجة الفورية.",
        descriptionEn: "Ability to stop messages via STOP keyword with immediate processing.",
      },
      {
        key: "optout",
        labelAr: "إلغاء الاشتراك",
        labelEn: "Opt-out",
        descriptionAr: "آلية واضحة لإلغاء الاشتراك وتسجيلها في السجل.",
        descriptionEn: "Clear opt-out mechanism recorded in the log.",
      },
    ],
  },
];

export function OutboundSafetyContent() {
  const locale = useLocale();
  const isAr = locale === "ar";

  return (
    <div className="space-y-6">
      {/* Top warning — no live send toggle */}
      <div className="flex items-start gap-3 rounded-xl border border-red-500/30 bg-red-500/5 p-4">
        <Lock className="size-5 text-red-400 shrink-0 mt-0.5" />
        <div className="text-sm text-red-200/90">
          {isAr
            ? "لا يوجد زر لتفعيل الإرسال الحي هنا. هذه الصفحة تعرض الحالة والتوثيق فقط. تفعيل الإرسال يتطلب تغيير متغيرات البيئة من قبل المؤسس بعد استيفاء كل البوابات."
            : "There is no live-send toggle here. This page displays status and documentation only. Enabling live send requires changing environment variables by the founder after all gates are met."}
        </div>
      </div>

      {/* Env flags */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <ShieldAlert className="size-5 text-amber-400" />
            {isAr ? "أعلام البيئة" : "Environment flags"}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-muted-foreground">
                  <th className="py-2 text-start font-medium">{isAr ? "العلم" : "Flag"}</th>
                  <th className="py-2 text-start font-medium">{isAr ? "الحالة الافتراضية" : "Default state"}</th>
                  <th className="py-2 text-start font-medium">{isAr ? "الوصف" : "Description"}</th>
                </tr>
              </thead>
              <tbody>
                {ENV_FLAGS.map((f) => (
                  <tr key={f.key} className="border-b border-border/50">
                    <td className="py-3 font-mono text-xs">{f.key}</td>
                    <td className="py-3">
                      <Badge variant={f.defaultValue ? "emerald" : "red"}>
                        {f.defaultValue
                          ? isAr ? "مفعّل" : "Enabled"
                          : isAr ? "معطّل" : "Disabled"}
                      </Badge>
                    </td>
                    <td className="py-3 text-muted-foreground">
                      {isAr ? f.descriptionAr : f.descriptionEn}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>

      {/* Channel readiness checklists */}
      <div className="grid gap-4 md:grid-cols-3">
        {CHANNEL_CHECKLISTS.map((ch) => {
          const Icon = ch.icon;
          return (
            <Card key={ch.channel}>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Icon className="size-4" />
                  {isAr ? ch.labelAr : ch.labelEn}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="space-y-3">
                  {ch.items.map((item) => (
                    <li key={item.key} className="space-y-1">
                      <div className="flex items-center gap-2">
                        <ShieldCheck className="size-4 text-muted-foreground/40" />
                        <span className="text-sm font-medium">
                          {isAr ? item.labelAr : item.labelEn}
                        </span>
                      </div>
                      <p className="text-xs text-muted-foreground ps-6">
                        {isAr ? item.descriptionAr : item.descriptionEn}
                      </p>
                    </li>
                  ))}
                </ul>
                <div className="mt-3 rounded-md bg-amber-500/5 p-2 text-xs text-amber-200/80">
                  {isAr
                    ? "كل البنود غير مكتملة افتراضياً. أكملها قبل أي إرسال."
                    : "All items incomplete by default. Complete them before any send."}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {/* Documentation note */}
      <Card className="border-border">
        <CardContent className="py-5">
          <p className="text-sm text-muted-foreground">
            {isAr
              ? "هذه الصفحة للعرض والتوثيق فقط. لا يمكن تفعيل الإرسال الحي من الواجهة — استخدم متغيرات البيئة بعد استيفاء كل بوابات الأمان والموافقة البشرية."
              : "This page is for display and documentation only. Live send cannot be enabled from the UI — use environment variables after all safety gates and human approval are satisfied."}
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

export default OutboundSafetyContent;