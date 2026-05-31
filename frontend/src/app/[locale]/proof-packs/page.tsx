import ProofPackTracker from "@/components/operations/ProofPackTracker";

type PageProps = { params: Promise<{ locale: string }> };

export default async function ProofPacksPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <ProofPackTracker locale={locale} />
    </main>
  );
}
