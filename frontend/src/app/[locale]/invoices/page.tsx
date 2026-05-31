import InvoiceDashboard from "@/components/operations/InvoiceDashboard";

type PageProps = { params: Promise<{ locale: string }> };

export default async function InvoicesPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <InvoiceDashboard locale={locale} />
    </main>
  );
}
