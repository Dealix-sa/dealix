import SubscriptionManager from "@/components/operations/SubscriptionManager";

export default function SubscriptionsPage({
  params,
}: {
  params: { locale: string };
}) {
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <SubscriptionManager locale={params.locale} />
    </main>
  );
}
