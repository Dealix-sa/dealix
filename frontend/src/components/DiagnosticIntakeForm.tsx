"use client";
import LeadCaptureForm from "./LeadCaptureForm";

export default function DiagnosticIntakeForm() {
  return (
    <section className="mx-auto max-w-3xl py-12">
      <h2 className="text-3xl font-bold mb-4">تشخيص إيرادي وتشغيلي</h2>
      <p className="mb-6 opacity-80">املأ النموذج وسنحوّل مشكلتك إلى خريطة فرص، فجوات، وأول workflow يستحق التنفيذ.</p>
      <LeadCaptureForm />
    </section>
  );
}
