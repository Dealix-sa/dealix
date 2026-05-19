import { getTranslations } from "next-intl/server";

import { AppLayout } from "@/components/layout/AppLayout";
import { ApprovalCenter } from "@/components/approvals/ApprovalCenter";
import { GovernedOpsControl } from "@/components/gtm/GovernedOpsControl";

interface Props {
  params: Promise<{ locale: string }>;
}

export default async function OpsApprovalsShell({ params }: Props) {
  const { locale } = await params;
  const tApprovals = await getTranslations({ locale, namespace: "approvals" });
  const tn = await getTranslations({ locale, namespace: "opsPages" });

  return (
    <AppLayout title={`Ops · ${tApprovals("title")}`} subtitle={tn("approvalsSubtitle")}>
      <div className="space-y-6">
        <GovernedOpsControl />
        <ApprovalCenter />
      </div>
    </AppLayout>
  );
}
