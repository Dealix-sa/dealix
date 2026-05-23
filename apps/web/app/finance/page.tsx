import { CashSnapshot } from "../../components/finance/CashSnapshot";
import type { FinanceSnapshot } from "../../lib/types";

// TODO: live wire — GET /api/v1/finance + /api/v1/revenue-pipeline
const snapshot: FinanceSnapshot = {
  cashSar: 0,
  mrrSar: 0,
  pipelineSar: 0,
  weightedPipelineSar: 0,
  paymentFollowUpsSar: 0,
  monthlyBurnSar: 0,
  runwayMonths: 0,
};

export default function FinancePage() {
  return (
    <main className="grid">
      <section>
        <h1>Finance</h1>
        <p style={{ maxWidth: 720 }}>
          أين الكاش؟ كم MRR؟ كم في الـpipeline؟ كم runway؟ القرارات الكبيرة تبدأ من هنا.
        </p>
      </section>
      <CashSnapshot snapshot={snapshot} />
    </main>
  );
}
