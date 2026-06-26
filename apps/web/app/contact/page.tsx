"use client";

import { useState } from "react";

export default function ContactPage() {
  const [status, setStatus] = useState<"idle" | "sending" | "done" | "error">("idle");

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setStatus("sending");
    const form = e.currentTarget;
    const data = {
      name: (form.elements.namedItem("name") as HTMLInputElement).value,
      company: (form.elements.namedItem("company") as HTMLInputElement).value,
      contact: (form.elements.namedItem("contact") as HTMLInputElement).value,
      message: (form.elements.namedItem("message") as HTMLTextAreaElement).value,
    };
    try {
      const res = await fetch("/api/v1/public/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      if (!res.ok) throw new Error("server error");
      setStatus("done");
    } catch {
      setStatus("error");
    }
  }

  return (
    <main className="min-h-screen bg-[#070A12] text-white">
      <div className="mx-auto max-w-xl px-6 py-20">
        <p className="text-xs uppercase tracking-[0.3em] text-amber-300/80">تواصل معنا · Contact</p>
        <h1 className="mt-4 text-4xl font-bold">نرد خلال 24 ساعة</h1>
        <p className="mt-3 text-sm text-white/60">
          أرسل رسالتك وسيراجعها المؤسس شخصياً — لا أتمتة، لا ردود آلية.
        </p>

        {status === "done" ? (
          <div className="mt-10 rounded-2xl border border-amber-300/30 bg-amber-300/5 p-8 text-center">
            <p className="text-xl font-semibold text-amber-200">وصلت رسالتك ✓</p>
            <p className="mt-2 text-sm text-white/60">
              سنتواصل معك خلال 24 ساعة. شكراً لثقتك.
            </p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="mt-10 space-y-5">
            <div>
              <label htmlFor="name" className="block text-xs text-white/50 mb-1">
                الاسم الكامل *
              </label>
              <input
                id="name"
                name="name"
                type="text"
                required
                minLength={2}
                maxLength={100}
                className="w-full rounded-lg border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 focus:border-amber-300/50 focus:outline-none"
                placeholder="محمد العلي"
              />
            </div>

            <div>
              <label htmlFor="company" className="block text-xs text-white/50 mb-1">
                اسم الشركة *
              </label>
              <input
                id="company"
                name="company"
                type="text"
                required
                minLength={2}
                maxLength={100}
                className="w-full rounded-lg border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 focus:border-amber-300/50 focus:outline-none"
                placeholder="شركة الرياض للتجارة"
              />
            </div>

            <div>
              <label htmlFor="contact" className="block text-xs text-white/50 mb-1">
                واتساب أو بريد إلكتروني *
              </label>
              <input
                id="contact"
                name="contact"
                type="text"
                required
                minLength={5}
                maxLength={200}
                className="w-full rounded-lg border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 focus:border-amber-300/50 focus:outline-none"
                placeholder="+966 5x xxx xxxx"
              />
            </div>

            <div>
              <label htmlFor="message" className="block text-xs text-white/50 mb-1">
                رسالتك *
              </label>
              <textarea
                id="message"
                name="message"
                required
                minLength={10}
                maxLength={2000}
                rows={5}
                className="w-full rounded-lg border border-white/15 bg-white/5 px-4 py-3 text-sm text-white placeholder-white/30 focus:border-amber-300/50 focus:outline-none resize-none"
                placeholder="كيف يمكننا مساعدتك؟"
              />
            </div>

            {status === "error" && (
              <p className="text-xs text-red-400">
                حدث خطأ، حاول مرة أخرى أو تواصل معنا مباشرة.
              </p>
            )}

            <button
              type="submit"
              disabled={status === "sending"}
              className="w-full rounded-lg bg-amber-300 px-6 py-3 text-sm font-semibold text-black hover:bg-amber-200 transition-colors disabled:opacity-50"
            >
              {status === "sending" ? "جاري الإرسال..." : "أرسل الرسالة"}
            </button>

            <p className="text-xs text-white/30 text-center">
              بياناتك لن تُشارك مع أي طرف ثالث · لا إرسال آلي · PDPL compliant
            </p>
          </form>
        )}
      </div>
    </main>
  );
}
