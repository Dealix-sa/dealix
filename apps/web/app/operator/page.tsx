"use client";

import PageShell from "@/components/PageShell";
import SectionHeader from "@/components/SectionHeader";
import CommandPanel from "@/components/CommandPanel";

export default function OperatorPage() {
  return (
    <PageShell>
      <section className="card dot-pattern" style={{ position: "relative", overflow: "hidden", paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">المشغّل</p>
        <h1 style={{ maxWidth: 860 }}>يومك التجاري في أمر واحد</h1>
        <p style={{ maxWidth: 680, fontSize: "1.15rem", lineHeight: 1.7 }}>
          Daily Operator يشغل تسلسل Dealix التجاري اليومي: فحص، استيراد، تصنيف، مسودات، تقارير.
        </p>
      </section>

      <section>
        <SectionHeader title="ما الذي يفعله Daily Operator؟" />
        <div className="cards">
          <CommandPanel title="١. فحص الأمان">
            <p>يفحص المستودع بحثاً عن أسرار أو مفاتيح API مسرّبة.</p>
          </CommandPanel>
          <CommandPanel title="٢. التحقق من النظام">
            <p>يتأكد من وجود الملفات الأساسية للتشغيل التجاري.</p>
          </CommandPanel>
          <CommandPanel title="٣. استيراد وتصنيف">
            <p>يستورد العملاء المحتملين ويصنفهم حسب Fit وPain وBudget وUrgency.</p>
          </CommandPanel>
          <CommandPanel title="٤. مسودات المتابعة">
            <p>ينشئ مسودات واتساب/بريد بانتظار المراجعة البشرية.</p>
          </CommandPanel>
          <CommandPanel title="٥. تقرير المؤسس">
            <p>يكتب ملخصاً يومياً للمؤسس بأهم القرارات المطلوبة.</p>
          </CommandPanel>
        </div>
      </section>
    </PageShell>
  );
}
