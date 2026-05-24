import { FounderPage } from "../../components/brand/founder-page";

export default function FinanceOpsPage() {
  return (
    <FounderPage
      title="Finance Ops"
      subtitle="Payment capture · invoicing · resource allocation."
      blocks={[
        { title: "Payment capture queue", body: <p>finance/payment_capture_queue.csv</p> },
        { title: "Resource allocation", body: <p>finance/resource_allocation.csv</p> },
        { title: "Capital allocation", body: <p>finance/capital_allocation.csv</p> },
      ]}
    />
  );
}
