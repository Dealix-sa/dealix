import TeamDashboard from "@/components/operations/TeamDashboard";

type PageProps = { params: Promise<{ locale: string }> };

export default async function TeamPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <TeamDashboard locale={locale} />
    </main>
  );
}
