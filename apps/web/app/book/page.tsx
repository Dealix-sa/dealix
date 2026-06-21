"use client";

import Link from "next/link";
import { useState } from "react";

const timeSlots = [
  "السبت ٩ص – ١٢م",
  "السبت ١م – ٤م",
  "الأحد ٩ص – ١٢م",
  "الأحد ١م – ٤م",
  "الاثنين ٩ص – ١٢م",
  "الاثنين ١م – ٤م",
  "الثلاثاء ٩ص – ١٢م",
  "الأربعاء ١م – ٤م",
];

const sectors = [
  "الرعاية الصحية",
  "الخدمات اللوجستية والتوزيع",
  "التطوير العقاري",
  "التدريب والتعليم",
  "المطاعم والضيافة",
  "التجارة والتجزئة",
  "التقنية والبرمجيات",
  "الاستشارات والخدمات المهنية",
  "البناء والمقاولات",
  "قطاع آخر",
];

const whatToExpect = [
  { icon: "🎯", text: "نحدد أكبر ٣ ثغرات في إيراد شركتك بأرقام دقيقة" },
  { icon: "🗺️", text: "نرسم خريطة واضحة للخطوات التالية — بدون غموض" },
  { icon: "📋", text: "تحصل على ملخص مكتوب خلال ٢٤ ساعة من الجلسة" },
  { icon: "🤝", text: "لا بيع، لا ضغط — فقط تشخيص صادق وعملي" },
];

export default function BookPage() {
  const [submitted, setSubmitted] = useState(false);
  const [form, setForm] = useState({
    name: "",
    company: "",
    phone: "",
    sector: "",
    team_size: "",
    time_pref: "",
    biggest_problem: "",
  });

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setSubmitted(true);
  }

  return (
    <main style={{ display: "flex", flexDirection: "column", gap: "var(--sp-12)", paddingBottom: "var(--sp-16)" }}>

      {/* Nav */}
      <nav className="navbar" aria-label="Primary navigation">
        <Link href="/" className="navbar-brand">Dealix</Link>
        <ul className="navbar-links" role="list">
          <li><Link href="/">الرئيسية</Link></li>
          <li><Link href="/offers">العروض</Link></li>
          <li><Link href="/pricing">التسعير</Link></li>
        </ul>
        <div className="actions" style={{ marginTop: 0 }}>
          <a href="https://wa.me/966500000000" className="btn btn-secondary" style={{ minHeight: 38, padding: "0 18px", fontSize: "0.85rem" }}>
            واتساب مباشر
          </a>
        </div>
      </nav>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))", gap: "var(--sp-8)", alignItems: "start" }}>

        {/* Left — Info */}
        <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-6)" }}>

          <section className="card dot-pattern" style={{ padding: "clamp(32px,5vw,56px)", position: "relative", overflow: "hidden" }}>
            <div aria-hidden="true" style={{
              position: "absolute", top: "-60px", right: "-60px",
              width: "300px", height: "300px",
              background: "radial-gradient(circle, rgba(212,175,55,0.10), transparent 65%)",
              pointerEvents: "none",
            }} />
            <p className="eyebrow">التشخيص المجاني</p>
            <h1 style={{ fontSize: "clamp(1.8rem,4vw,2.8rem)", marginBottom: "var(--sp-4)" }}>
              احجز جلستك<br />
              <span className="gradient-text">المجانية الآن</span>
            </h1>
            <p style={{ color: "rgba(255,255,255,0.65)", lineHeight: 1.8, fontSize: "0.95rem" }}>
              ٣٠ دقيقة مع المؤسس مباشرة. تخرج بخريطة واضحة لأكبر ٣ ثغرات في إيراد شركتك وخطوة عملية يمكنك تطبيقها غداً.
            </p>
          </section>

          <section className="card" style={{ padding: "var(--sp-8) var(--sp-6)" }}>
            <h2 style={{ fontSize: "1.1rem", marginBottom: "var(--sp-5)" }}>ماذا يحدث في الجلسة؟</h2>
            <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-4)" }}>
              {whatToExpect.map(({ icon, text }) => (
                <div key={text} style={{ display: "flex", gap: "var(--sp-3)", alignItems: "flex-start" }}>
                  <span style={{ fontSize: "1.3rem", flexShrink: 0 }}>{icon}</span>
                  <p style={{ fontSize: "0.90rem", color: "rgba(255,255,255,0.70)", lineHeight: 1.65 }}>{text}</p>
                </div>
              ))}
            </div>
          </section>

          <section className="card" style={{ padding: "var(--sp-6)", background: "rgba(16,185,129,0.06)", border: "1px solid rgba(16,185,129,0.2)" }}>
            <p style={{ fontSize: "0.88rem", fontWeight: 700, color: "#10B981", marginBottom: "var(--sp-3)" }}>أو تواصل مباشرة عبر واتساب</p>
            <a
              href="https://wa.me/966500000000?text=السلام عليكم، أريد حجز تشخيص مجاني مع Dealix"
              style={{
                display: "inline-flex", alignItems: "center", gap: "var(--sp-2)",
                background: "#25D366", color: "#fff",
                padding: "10px 20px", borderRadius: "var(--r-pill)",
                fontWeight: 600, fontSize: "0.88rem", textDecoration: "none",
              }}
            >
              <span>💬</span>
              تواصل عبر واتساب
            </a>
            <p style={{ fontSize: "0.80rem", color: "rgba(255,255,255,0.40)", marginTop: "var(--sp-3)" }}>
              عادةً نرد خلال ساعة في أوقات الدوام
            </p>
          </section>

        </div>

        {/* Right — Form */}
        <div>
          {submitted ? (
            <div
              className="card"
              style={{
                padding: "clamp(40px,6vw,64px)",
                textAlign: "center",
                border: "2px solid rgba(16,185,129,0.3)",
                background: "rgba(16,185,129,0.05)",
              }}
            >
              <div style={{ fontSize: "3rem", marginBottom: "var(--sp-4)" }}>✅</div>
              <h2 style={{ color: "#10B981", marginBottom: "var(--sp-3)", fontSize: "1.5rem" }}>
                تم الاستلام!
              </h2>
              <p style={{ color: "rgba(255,255,255,0.70)", lineHeight: 1.8, maxWidth: "380px", margin: "0 auto" }}>
                شكراً {form.name}. سيتواصل معك الفريق خلال ٢٤ ساعة لتأكيد موعد التشخيص.
              </p>
              <p style={{ marginTop: "var(--sp-4)", color: "rgba(255,255,255,0.45)", fontSize: "0.85rem" }}>
                إذا أردت تسريع الأمر — راسلنا على واتساب مباشرة.
              </p>
              <a
                href="https://wa.me/966500000000"
                style={{
                  display: "inline-block", marginTop: "var(--sp-5)",
                  background: "#25D366", color: "#fff",
                  padding: "10px 24px", borderRadius: "var(--r-pill)",
                  fontWeight: 600, fontSize: "0.88rem", textDecoration: "none",
                }}
              >
                واتساب مباشر →
              </a>
            </div>
          ) : (
            <form
              onSubmit={handleSubmit}
              className="card"
              style={{ padding: "clamp(24px,4vw,40px)", display: "flex", flexDirection: "column", gap: "var(--sp-5)" }}
            >
              <div>
                <h2 style={{ fontSize: "1.2rem", marginBottom: "var(--sp-2)" }}>بيانات الحجز</h2>
                <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.45)" }}>سيتواصل معك الفريق لتأكيد الموعد خلال ٢٤ ساعة</p>
              </div>

              {/* Name */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="name" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  الاسم الكامل *
                </label>
                <input
                  id="name"
                  name="name"
                  type="text"
                  required
                  placeholder="محمد العتيبي"
                  value={form.name}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>

              {/* Company */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="company" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  اسم الشركة *
                </label>
                <input
                  id="company"
                  name="company"
                  type="text"
                  required
                  placeholder="شركة النور للتوزيع"
                  value={form.company}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>

              {/* Phone */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="phone" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  رقم الواتساب *
                </label>
                <input
                  id="phone"
                  name="phone"
                  type="tel"
                  required
                  placeholder="+966 50 000 0000"
                  value={form.phone}
                  onChange={handleChange}
                  style={inputStyle}
                />
              </div>

              {/* Sector */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="sector" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  القطاع *
                </label>
                <select
                  id="sector"
                  name="sector"
                  required
                  value={form.sector}
                  onChange={handleChange}
                  style={{ ...inputStyle, cursor: "pointer" }}
                >
                  <option value="">اختر القطاع</option>
                  {sectors.map((s) => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>

              {/* Team Size */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="team_size" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  حجم الفريق *
                </label>
                <select
                  id="team_size"
                  name="team_size"
                  required
                  value={form.team_size}
                  onChange={handleChange}
                  style={{ ...inputStyle, cursor: "pointer" }}
                >
                  <option value="">اختر</option>
                  <option value="1-5">١–٥ موظفين</option>
                  <option value="6-20">٦–٢٠ موظف</option>
                  <option value="21-50">٢١–٥٠ موظف</option>
                  <option value="51+">٥١+ موظف</option>
                </select>
              </div>

              {/* Time Preference */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="time_pref" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  الوقت المفضل للجلسة
                </label>
                <select
                  id="time_pref"
                  name="time_pref"
                  value={form.time_pref}
                  onChange={handleChange}
                  style={{ ...inputStyle, cursor: "pointer" }}
                >
                  <option value="">أي وقت مناسب</option>
                  {timeSlots.map((t) => (
                    <option key={t} value={t}>{t}</option>
                  ))}
                </select>
              </div>

              {/* Problem */}
              <div style={{ display: "flex", flexDirection: "column", gap: "var(--sp-2)" }}>
                <label htmlFor="biggest_problem" style={{ fontSize: "0.85rem", fontWeight: 600, color: "rgba(255,255,255,0.70)" }}>
                  أكبر تحدٍّ تواجهه الآن؟ *
                </label>
                <textarea
                  id="biggest_problem"
                  name="biggest_problem"
                  required
                  rows={3}
                  placeholder="مثلاً: الاستفسارات تضيع في الواتساب ولا أعرف معدل التحويل الفعلي..."
                  value={form.biggest_problem}
                  onChange={handleChange}
                  style={{ ...inputStyle, resize: "vertical", minHeight: "90px", lineHeight: 1.6 }}
                />
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                style={{ width: "100%", fontSize: "1rem", padding: "14px", minHeight: 52 }}
              >
                احجز جلستي المجانية →
              </button>

              <p style={{ fontSize: "0.78rem", color: "rgba(255,255,255,0.35)", textAlign: "center", lineHeight: 1.6 }}>
                لا نشارك بياناتك مع أي طرف ثالث. متوافق مع PDPL.
              </p>
            </form>
          )}
        </div>

      </div>

      {/* FAQ Quick */}
      <section>
        <h2 style={{ marginBottom: "var(--sp-6)" }}>أسئلة سريعة</h2>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: "var(--sp-4)" }}>
          {[
            ["هل الجلسة مجانية فعلاً؟", "نعم. ٠ ريال، بلا بطاقة ائتمانية، بلا التزامات."],
            ["أين تحدث الجلسة؟", "واتساب أو زووم — حسب ما يناسبك."],
            ["هل أحتاج تحضير شيء؟", "لا. فقط فكّر: ما أكبر شيء يستنزف وقت فريقك اليوم؟"],
            ["متى ترد عليّ؟", "خلال ٢٤ ساعة. إذا أردت أسرع — راسلنا على واتساب."],
          ].map(([q, a]) => (
            <div
              key={q}
              className="card"
              style={{ padding: "var(--sp-5) var(--sp-6)" }}
            >
              <p style={{ fontWeight: 700, fontSize: "0.92rem", marginBottom: "var(--sp-2)", color: "var(--dealix-gold)" }}>
                {q}
              </p>
              <p style={{ fontSize: "0.88rem", color: "rgba(255,255,255,0.65)", lineHeight: 1.65 }}>{a}</p>
            </div>
          ))}
        </div>
      </section>

    </main>
  );
}

const inputStyle: React.CSSProperties = {
  width: "100%",
  background: "rgba(255,255,255,0.05)",
  border: "1px solid rgba(255,255,255,0.12)",
  borderRadius: "var(--r-md)",
  color: "#fff",
  padding: "12px 16px",
  fontSize: "0.92rem",
  fontFamily: "var(--font-body)",
  outline: "none",
  direction: "rtl",
};
