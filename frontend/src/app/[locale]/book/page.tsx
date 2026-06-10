import LeadCaptureForm from "../../../components/LeadCaptureForm";

export default function BookPage() {
  return (
    <main className="min-h-screen bg-[#07111f] text-white px-6 py-20">
      <section className="mx-auto max-w-4xl">
        <h1 className="text-5xl font-black">احجز جلسة Dealix</h1>
        <p className="mt-5 text-xl opacity-80">اكتب المشكلة وسنحدد هل تبدأ بـ Diagnostic، Pilot، أو Custom AI System.</p>
        <div className="mt-10"><LeadCaptureForm /></div>
      </section>
    </main>
  );
}
