import { useState } from "react";
import { trpc } from "@/providers/trpc";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { ArrowLeft, BarChart3, CalendarClock, CheckCircle } from "lucide-react";

export default function Booking() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    company: "",
    role: "",
    website: "",
    pain: "",
    currentSystems: "",
    consentEmail: false,
    scheduledAt: "",
  });

  const booking = trpc.booking.create.useMutation({
    onSuccess: () => setSubmitted(true),
  });

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    booking.mutate(formData);
  };

  return (
    <div className="min-h-screen bg-[#F0F9F8]" dir="rtl">
      <nav className="flex items-center justify-between border-b border-[#15807A]/20 bg-[#0A1F1E] px-6 py-4">
        <a href="/" className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-[#15807A]">
            <BarChart3 className="h-5 w-5 text-white" />
          </div>
          <span className="text-lg font-bold text-white">Dealix</span>
        </a>
        <a
          href="/"
          className="flex items-center gap-1 text-sm text-[#E8F4F3] transition-colors hover:text-white"
        >
          <ArrowLeft className="h-4 w-4" />
          العودة للرئيسية
        </a>
      </nav>

      <div className="mx-auto max-w-5xl px-4 py-12 sm:px-6">
        <div className="grid gap-8 lg:grid-cols-[1.2fr_0.8fr]">
          <Card className="border-[#E8F4F3] bg-white shadow-sm">
            <CardHeader className="text-center">
              <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-[#E8F4F3]">
                <CalendarClock className="h-7 w-7 text-[#15807A]" />
              </div>
              <CardTitle className="text-2xl text-[#0A1F1E]">
                احجز تشخيص Dealix
              </CardTitle>
              <CardDescription className="mt-2 text-[#4A6B69]">
                جلسة تشخيص قصيرة لفهم وضع الإيرادات والمتابعة والـ WhatsApp
                والقرار داخل الشركة قبل اقتراح المسار الأنسب.
              </CardDescription>
            </CardHeader>

            {!submitted ? (
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-5">
                  <div>
                    <Label className="text-sm text-[#0A1F1E]">
                      الاسم الكامل *
                    </Label>
                    <Input
                      required
                      placeholder="أحمد آل راشد"
                      value={formData.name}
                      onChange={(event) =>
                        setFormData({ ...formData, name: event.target.value })
                      }
                      className="mt-1 border-[#E8F4F3]"
                    />
                  </div>

                  <div className="grid gap-4 md:grid-cols-2">
                    <div>
                      <Label className="text-sm text-[#0A1F1E]">
                        اسم الشركة *
                      </Label>
                      <Input
                        required
                        placeholder="Example Co"
                        value={formData.company}
                        onChange={(event) =>
                          setFormData({
                            ...formData,
                            company: event.target.value,
                          })
                        }
                        className="mt-1 border-[#E8F4F3]"
                      />
                    </div>
                    <div>
                      <Label className="text-sm text-[#0A1F1E]">
                        الدور الحالي *
                      </Label>
                      <Input
                        required
                        placeholder="Founder / CRO / CEO"
                        value={formData.role}
                        onChange={(event) =>
                          setFormData({ ...formData, role: event.target.value })
                        }
                        className="mt-1 border-[#E8F4F3]"
                      />
                    </div>
                  </div>

                  <div>
                    <Label className="text-sm text-[#0A1F1E]">
                      الموقع الإلكتروني
                    </Label>
                    <Input
                      placeholder="https://example.sa"
                      value={formData.website}
                      onChange={(event) =>
                        setFormData({
                          ...formData,
                          website: event.target.value,
                        })
                      }
                      className="mt-1 border-[#E8F4F3]"
                    />
                  </div>

                  <div>
                    <Label className="text-sm text-[#0A1F1E]">
                      أين المشكلة الأكبر الآن؟
                    </Label>
                    <Select
                      value={formData.pain}
                      onValueChange={(value) =>
                        setFormData({ ...formData, pain: value })
                      }
                    >
                      <SelectTrigger className="mt-1 border-[#E8F4F3]">
                        <SelectValue placeholder="اختر التحدي الرئيسي" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="leads">
                          ضعف lead flow أو ضعف الوصول للفرص
                        </SelectItem>
                        <SelectItem value="followup">
                          المتابعة تتأخر أو تضيع
                        </SelectItem>
                        <SelectItem value="reporting">
                          لا توجد رؤية تشغيلية يومية واضحة
                        </SelectItem>
                        <SelectItem value="whatsapp">
                          محادثات WhatsApp غير منظمة
                        </SelectItem>
                        <SelectItem value="brain">
                          القرارات موزعة وغير موثقة
                        </SelectItem>
                        <SelectItem value="other">أخرى</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label className="text-sm text-[#0A1F1E]">
                      الأنظمة الحالية
                    </Label>
                    <Select
                      value={formData.currentSystems}
                      onValueChange={(value) =>
                        setFormData({ ...formData, currentSystems: value })
                      }
                    >
                      <SelectTrigger className="mt-1 border-[#E8F4F3]">
                        <SelectValue placeholder="اختر النظام الحالي" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="excel">Excel / Sheets</SelectItem>
                        <SelectItem value="crm">CRM</SelectItem>
                        <SelectItem value="whatsapp_only">
                          WhatsApp فقط
                        </SelectItem>
                        <SelectItem value="notion">Notion / Docs</SelectItem>
                        <SelectItem value="mixed">
                          أنظمة متفرقة غير مترابطة
                        </SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="consent"
                      checked={formData.consentEmail}
                      onChange={(event) =>
                        setFormData({
                          ...formData,
                          consentEmail: event.target.checked,
                        })
                      }
                      className="h-4 w-4 accent-[#15807A]"
                    />
                    <Label
                      htmlFor="consent"
                      className="cursor-pointer text-sm text-[#4A6B69]"
                    >
                      أوافق على تواصل Dealix معي بخصوص هذا الطلب فقط.
                    </Label>
                  </div>

                  <Button
                    type="submit"
                    disabled={booking.isPending}
                    className="h-12 w-full bg-[#15807A] text-base hover:bg-[#0F5F5A]"
                  >
                    {booking.isPending
                      ? "جاري إرسال الطلب..."
                      : "احجز جلسة التشخيص"}
                  </Button>
                </form>
              </CardContent>
            ) : (
              <CardContent className="py-12 text-center">
                <CheckCircle className="mx-auto mb-4 h-16 w-16 text-[#15807A]" />
                <h3 className="mb-2 text-xl font-bold text-[#0A1F1E]">
                  تم إرسال الطلب بنجاح
                </h3>
                <p className="mb-6 text-[#4A6B69]">
                  سنراجع الطلب ونقترح المسار الأنسب: Sprint أو Build أو
                  Operating Partner.
                </p>
                <a href="/">
                  <Button className="bg-[#15807A] text-white hover:bg-[#0F5F5A]">
                    العودة للرئيسية
                  </Button>
                </a>
              </CardContent>
            )}
          </Card>

          <div className="space-y-6">
            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="text-[#0A1F1E]">
                  ماذا يحدث بعد الحجز؟
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-3 text-sm text-[#4A6B69]">
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  1. مراجعة الوضع الحالي والأنظمة الموجودة.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  2. تحديد أكبر bottleneck في الإيرادات أو المتابعة.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  3. اقتراح النظام الأنسب للبدء: Command Room أو Brain أو
                  WhatsApp.
                </div>
                <div className="rounded-lg bg-[#F0F9F8] p-3">
                  4. تقديم scope واضح بدون وعود مبالغ فيها.
                </div>
              </CardContent>
            </Card>

            <Card className="border-[#E8F4F3] bg-white">
              <CardHeader>
                <CardTitle className="text-[#0A1F1E]">إشارات الثقة</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {[
                  {
                    label: "لا إرسال آلي",
                    desc: "كل outbound يمر بمراجعة بشرية.",
                  },
                  {
                    label: "قناة WhatsApp رسمية",
                    desc: "Cloud API + webhooks + approvals.",
                  },
                  {
                    label: "امتثال مدمج",
                    desc: "PDPL + AI governance + auditability.",
                  },
                ].map((item) => (
                  <div key={item.label} className="rounded-lg bg-[#F0F9F8] p-3">
                    <p className="text-sm font-bold text-[#0A1F1E]">
                      {item.label}
                    </p>
                    <p className="mt-1 text-xs text-[#4A6B69]">{item.desc}</p>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}