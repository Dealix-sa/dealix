"use client";

import { useState } from "react";

export default function LandingPage() {
  const [email, setEmail] = useState("");
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-white" dir="rtl">
      {/* Navbar */}
      <nav className="border-b border-slate-100">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="text-2xl font-bold text-emerald-600">Dealix</div>
          <div className="hidden md:flex gap-8 text-sm text-slate-600">
            <a href="#features" className="hover:text-emerald-600 transition">المميزات</a>
            <a href="#pricing" className="hover:text-emerald-600 transition">الأسعار</a>
            <a href="#zatca" className="hover:text-emerald-600 transition">ZATCA</a>
          </div>
          <a href="/signup" className="bg-emerald-600 text-white px-5 py-2 rounded-lg text-sm font-medium hover:bg-emerald-700 transition">
            ابدأ مجاناً
          </a>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-20 text-center">
        <div className="inline-flex items-center gap-2 bg-emerald-50 text-emerald-700 px-4 py-2 rounded-full text-sm font-medium mb-8">
          <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span>
          🇸🇦 أول ERP SaaS سعودي شامل
        </div>
        <h1 className="text-4xl md:text-6xl font-bold text-slate-900 mb-6 leading-tight">
          نظام تشغيل <span className="text-emerald-600">شركتك السعودية</span>
        </h1>
        <p className="text-lg md:text-xl text-slate-500 max-w-2xl mx-auto mb-10">
          CRM + Projects + HR + Inventory + Finance — كل شي في منصة واحدة.
          ZATCA جاهز. PDPL أصلاً. بالعربي. بالريال.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a href="/signup" className="bg-emerald-600 text-white px-8 py-4 rounded-xl text-lg font-semibold hover:bg-emerald-700 transition shadow-lg shadow-emerald-200">
            ابدأ مجاناً — شهر كامل
          </a>
          <a href="#demo" className="bg-white text-slate-700 border border-slate-200 px-8 py-4 rounded-xl text-lg font-semibold hover:bg-slate-50 transition">
            احجز demo
          </a>
        </div>
        <p className="text-sm text-slate-400 mt-4">لا بطاقة ائتمان. لا التزام. ألغي متى تبي.</p>
      </section>

      {/* Logos / Social Proof */}
      <section className="border-y border-slate-100 py-12">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <p className="text-sm text-slate-400 mb-6">بُني للسوق السعودي — ليس تعديل أجنبي</p>
          <div className="flex flex-wrap justify-center gap-8 text-slate-300 font-bold text-xl">
            <span>Zoho ❌</span>
            <span>HubSpot ❌</span>
            <span>QuickBooks ❌</span>
            <span className="text-emerald-600">Dealix ✅</span>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="max-w-6xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center text-slate-900 mb-4">كل شي تحتاجه — في مكان واحد</h2>
        <p className="text-center text-slate-500 mb-12">لا حاجة لـ 5 أدوات منفصلة</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[
            { icon: "👥", title: "CRM", desc: "إدارة العملاء والمبيعات والصفقات من A to Z" },
            { icon: "📋", title: "Projects", desc: "مشاريع، مهام، Gantt chart، time tracking" },
            { icon: "🎧", title: "Support Desk", desc: "تذاكر دعم، SLA، knowledge base" },
            { icon: "👔", title: "HR", desc: "موظفين، حضور، إجازات، رواتب مع GOSI" },
            { icon: "📦", title: "Inventory", desc: "مخزون، مستودعات، مشتريات، موردين" },
            { icon: "💰", title: "Finance", desc: "محاسبة، فواتير، ZATCA e-invoicing" },
          ].map((f) => (
            <div key={f.title} className="bg-slate-50 p-6 rounded-xl hover:shadow-md transition">
              <div className="text-3xl mb-3">{f.icon}</div>
              <h3 className="font-bold text-slate-900 mb-2">{f.title}</h3>
              <p className="text-sm text-slate-500">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ZATCA Section */}
      <section id="zatca" className="bg-slate-900 text-white py-20">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">ZATCA الفوترة الإلكترونية — جاهز من اليوم الأول</h2>
          <p className="text-slate-300 max-w-2xl mx-auto mb-10">
            المرحلة الثانية (Phase 2) تتطلب إرسال كل فاتورة B2B لـ ZATCA في real-time.
            Dealix يعمل كل هذا تلقائياً — QR code، XML، توقيع رقمي، إبلاغ فوري.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {[
              { title: "QR Code", desc: "توليد QR code تلقائي على كل فاتورة" },
              { title: "UBL 2.1 XML", desc: "تنسيق موحد متوافق مع ZATCA" },
              { title: "Real-time Clearing", desc: "إرسال واعتماد فوري من الهيئة" },
            ].map((item) => (
              <div key={item.title} className="bg-slate-800 p-6 rounded-xl">
                <h3 className="font-bold text-emerald-400 mb-2">{item.title}</h3>
                <p className="text-sm text-slate-300">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing */}
      <section id="pricing" className="max-w-6xl mx-auto px-6 py-20">
        <h2 className="text-3xl font-bold text-center text-slate-900 mb-4">تسعير بسيط وشفاف</h2>
        <p className="text-center text-slate-500 mb-12">بدون رسوم خفية. بدون عقود طويلة.</p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { name: "مجاني", price: "0", period: "", desc: "للتجربة", features: ["1 مستخدم", "100 lead", "CRM فقط", "دعم المجتمع"] },
            { name: "بداية", price: "299", period: "/شهر", desc: "للشركات الصغيرة", features: ["3 مستخدمين", "1,000 lead", "CRM + Projects", "Support Desk", "ZATCA"], popular: true },
            { name: "نمو", price: "799", period: "/شهر", desc: "للشركات المتوسطة", features: ["10 مستخدمين", "10,000 lead", "كل الوحدات", "API Access", "AI Co-Pilot", "دعم مباشر"] },
          ].map((plan) => (
            <div key={plan.name} className={`p-6 rounded-xl border-2 ${plan.popular ? "border-emerald-500 bg-emerald-50" : "border-slate-200"} relative`}>
              {plan.popular && (
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 bg-emerald-600 text-white text-xs px-3 py-1 rounded-full font-medium">
                  الأكثر شيوعاً
                </div>
              )}
              <h3 className="font-bold text-lg text-slate-900">{plan.name}</h3>
              <p className="text-sm text-slate-500 mb-4">{plan.desc}</p>
              <div className="flex items-baseline gap-1 mb-6">
                <span className="text-4xl font-bold text-slate-900">{plan.price}</span>
                <span className="text-slate-500">ريال</span>
                <span className="text-sm text-slate-400">{plan.period}</span>
              </div>
              <ul className="space-y-2 mb-6">
                {plan.features.map((feat) => (
                  <li key={feat} className="flex items-center gap-2 text-sm text-slate-600">
                    <span className="text-emerald-500">✓</span> {feat}
                  </li>
                ))}
              </ul>
              <a href="/signup" className={`block text-center py-3 rounded-lg font-medium transition ${plan.popular ? "bg-emerald-600 text-white hover:bg-emerald-700" : "bg-slate-100 text-slate-700 hover:bg-slate-200"}`}>
                ابدأ الآن
              </a>
            </div>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="bg-emerald-600 text-white py-20">
        <div className="max-w-3xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-4">جاهز تبني نظام تشغيل لشركتك؟</h2>
          <p className="text-emerald-100 mb-8">ابدأ مجاناً لمدة شهر. لا بطاقة ائتمان. لا التزام.</p>
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3 max-w-md mx-auto">
            <input
              type="email"
              placeholder="بريدك الإلكتروني"
              className="flex-1 px-4 py-3 rounded-lg text-slate-900 focus:outline-none"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <button type="submit" className="bg-slate-900 text-white px-6 py-3 rounded-lg font-medium hover:bg-slate-800 transition">
              {submitted ? "تم! راجع بريدك" : "ابدأ مجاناً"}
            </button>
          </form>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-100 py-12">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-xl font-bold text-emerald-600">Dealix</div>
          <div className="text-sm text-slate-400">
            © 2026 Dealix. نظام تشغيل الشركة السعودية. 🇸🇦
          </div>
        </div>
      </footer>
    </div>
  );
}
