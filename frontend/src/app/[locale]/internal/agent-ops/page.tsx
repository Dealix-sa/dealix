export default function AgentOpsPage() {
  return (
    <main className="mx-auto max-w-5xl px-6 py-16">
      <h1 className="text-4xl font-bold">Internal Agent Operations</h1>
      <p className="mt-4 text-neutral-600">هذه الصفحة تعرض مبادئ تشغيل وكلاء Dealix: لا إرسال تلقائي، لا وعود مضمونة، ولا بيانات حساسة بدون موافقة.</p>
      <div className="mt-8 rounded-2xl border p-6">
        <h2 className="font-semibold">Human-in-the-loop by default</h2>
        <p className="mt-2 text-sm text-neutral-500">Agents draft, score, summarize, and recommend. Humans approve external actions.</p>
      </div>
    </main>
  );
}
