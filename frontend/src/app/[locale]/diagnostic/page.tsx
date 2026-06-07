import DiagnosticIntakeForm from "../../../components/DiagnosticIntakeForm";

export default function DiagnosticPage() {
  return (
    <main className="min-h-screen bg-[#07111f] text-white px-6">
      <section className="mx-auto max-w-5xl py-20">
        <p className="uppercase tracking-[0.3em] text-sm opacity-70">Dealix Diagnostic</p>
        <h1 className="text-5xl font-black mt-4">حوّل فوضى المتابعة والبيانات إلى خطة إيراد قابلة للتنفيذ.</h1>
        <p className="mt-6 text-xl opacity-80">التشخيص لا يبيعك AI عام؛ يحدد أين يضيع المال، ما أول workflow، وما الدليل المطلوب قبل التوسع.</p>
      </section>
      <DiagnosticIntakeForm />
    </main>
  );
}
