"use client";

import PageShell from "@/components/PageShell";
import { CONTACT_EMAIL, mailtoLink } from "@/lib/contact";

export default function LegalPage() {
  return (
    <PageShell>
      <section className="card" style={{ paddingTop: "clamp(40px,6vw,72px)", paddingBottom: "clamp(40px,6vw,72px)" }}>
        <p className="eyebrow">الشروط والخصوصية</p>
        <h1>الإطار القانوني</h1>
        <p>
          Dealix يلتزم بأنظمة حماية البيانات الشخصية في المملكة العربية السعودية (PDPL).
          لا نبيع البيانات. لا نرسل رسائل تلقائية بدون مراجعة.
        </p>
        <h3>سياسة الاحتفاظ بالبيانات</h3>
        <ul>
          <li>بيانات العملاء المحتملين: سنتان أو حتى إلغاء الاشتراك</li>
          <li>العقود والعروض: سبع سنوات</li>
          <li>المسودات المولدة بالذكاء الاصطناعي: ٩٠ يوماً</li>
        </ul>
        <h3>التواصل</h3>
        <p>
          لأي استفسار قانوني:{" "}
          <a href={mailtoLink("استفسار قانوني")} dir="ltr">{CONTACT_EMAIL}</a>
        </p>
      </section>
    </PageShell>
  );
}
