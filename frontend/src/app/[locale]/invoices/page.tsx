import InvoiceDashboard from "@/components/operations/InvoiceDashboard";

export default function InvoicesPage({ params }: { params: { locale: string } }) {
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <InvoiceDashboard locale={params.locale} />
    </main>
  );
}
