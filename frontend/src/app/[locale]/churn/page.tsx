import ChurnDashboard from "@/components/operations/ChurnDashboard";

export default function ChurnPage({ params }: { params: { locale: string } }) {
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <ChurnDashboard locale={params.locale} />
    </main>
  );
}
