import ProofPackTracker from "@/components/operations/ProofPackTracker";

export default function ProofPacksPage({ params }: { params: { locale: string } }) {
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <ProofPackTracker locale={params.locale} />
    </main>
  );
}
