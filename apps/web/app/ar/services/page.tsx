import type { Metadata } from "next";
import ServicesView from "../../../components/ServicesView";

export const metadata: Metadata = {
  title: "الخدمات — تشغيل إيراد بالذكاء الاصطناعي للشركات السعودية",
  description:
    "خدمات Dealix: تشخيص مجاني، سبرنت إثبات الإيرادات بـ٤٩٩ ريال، حزمة البيانات إلى الإيراد، تشغيل النمو الشهري، غرفة القيادة التنفيذية، وعرض Command Sprint بقيادة المؤسس. approval-first وملتزم بـ PDPL.",
  alternates: { canonical: "/ar/services", languages: { "ar-SA": "/ar/services", "en-US": "/services" } },
};

export default function ArabicServicesPage() {
  return <ServicesView locale="ar" />;
}
