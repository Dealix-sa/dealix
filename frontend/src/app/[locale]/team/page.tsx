import TeamDashboard from "@/components/operations/TeamDashboard";

export default function TeamPage({
  params,
}: {
  params: { locale: string };
}) {
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <TeamDashboard locale={params.locale} />
    </main>
  );
}
