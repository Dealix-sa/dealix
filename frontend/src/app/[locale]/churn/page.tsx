import ChurnDashboard from "@/components/operations/ChurnDashboard";

type PageProps = { params: Promise<{ locale: string }> };

export default async function ChurnPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <ChurnDashboard locale={locale} />
    </main>
  );
}
