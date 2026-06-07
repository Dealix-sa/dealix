import type { Metadata } from "next";
import CustomRequestForm from "../../components/CustomRequestForm";
import { VALUE_DISCLAIMER } from "../../lib/offerings";

export const metadata: Metadata = {
  title: "Custom AI — Tell us what to build",
  description:
    "Describe your challenge and we'll design a custom, approval-first AI revenue solution for your Saudi B2B company. No scraping, no auto-send, no guaranteed outcomes.",
  alternates: { canonical: "/custom", languages: { "ar-SA": "/ar/custom", "en-US": "/custom" } },
};

const STEPS = [
  ["1", "You describe the challenge", "Tell us what you want to build or fix — in your own words."],
  ["2", "We scope it, approval-first", "We map it to a governed workflow. Nothing external is sent or charged without your approval."],
  ["3", "You get a clear next step", "A free diagnostic, a Command Sprint, or a monthly plan — with evidence, not promises."],
];

export default function CustomPage() {
  return (
    <main dir="ltr" className="min-h-screen bg-[#06111f] text-white">
      <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
        <a href="/" className="text-lg font-black text-white">Dealix</a>
        <nav className="flex items-center gap-5 text-sm text-slate-400">
          <a href="/services" className="hover:text-white">Services</a>
          <a href="/ar/custom" className="hover:text-white">العربية</a>
        </nav>
      </header>

      <section className="mx-auto max-w-5xl px-6 pt-10 pb-8 md:pt-14">
        <p className="mb-5 inline-flex rounded-full border border-cyan-300/30 px-4 py-2 text-sm text-cyan-100">
          Custom AI · Approval-first
        </p>
        <h1 className="max-w-3xl text-4xl font-black leading-[1.15] md:text-5xl">
          Tell us what to build.
        </h1>
        <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
          Didn't find the exact fit in our services? Describe your challenge and we'll design a
          custom solution on the same principle: the AI drafts and analyses, you approve and send.
        </p>
      </section>

      <section className="mx-auto max-w-5xl px-6 pb-6">
        <div className="grid gap-4 md:grid-cols-3">
          {STEPS.map(([n, title, body]) => (
            <div key={n} className="rounded-3xl border border-white/10 bg-white/[0.03] p-6">
              <p className="text-sm font-black text-cyan-300">{n}</p>
              <h3 className="mt-2 text-base font-black text-slate-100">{title}</h3>
              <p className="mt-2 text-sm leading-7 text-slate-400">{body}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="mx-auto max-w-2xl px-6 pb-20 pt-6">
        <CustomRequestForm locale="en" />
        <p className="mt-8 text-center text-xs text-slate-500">{VALUE_DISCLAIMER}</p>
      </section>
    </main>
  );
}
