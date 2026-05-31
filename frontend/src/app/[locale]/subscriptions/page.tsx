import SubscriptionManager from "@/components/operations/SubscriptionManager";

type PageProps = { params: Promise<{ locale: string }> };

export default async function SubscriptionsPage({ params }: PageProps) {
  const { locale } = await params;
  return (
    <main className="min-h-screen bg-gray-50 p-6">
      <SubscriptionManager locale={locale} />
    </main>
  );
}
