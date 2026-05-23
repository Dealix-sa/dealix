export default function WorkersPage() {
  return (
    <main className="min-h-screen p-8">
      <h1 className="text-4xl font-bold">Worker Health</h1>
      <p className="mt-2 max-w-3xl">
        Monitor Dealix 24/7 machines: last run, status, failures, and queue backlog.
      </p>
      <section className="mt-8 rounded-2xl border p-6">
        <p>No worker data connected yet.</p>
      </section>
    </main>
  );
}
