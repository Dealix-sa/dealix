/**
 * Mandatory safe-disclaimer block.
 * variant="educational" is required on the Revenue Leakage Calculator:
 * estimates are educational and not a guarantee.
 */
export function Disclaimer({
  locale,
  variant = "default",
}: {
  locale: string;
  variant?: "default" | "educational";
}) {
  const isAr = locale === "ar";

  const text =
    variant === "educational"
      ? isAr
        ? "هذه تقديرات تعليمية لمساعدتك على ترتيب أولوياتك، وليست ضماناً أو وعداً بنتائج. الأرقام الفعلية تعتمد على بياناتك وقرارات فريقك."
        : "These are educational estimates to help you prioritize — not a guarantee or a promise of results. Actual numbers depend on your data and your team's decisions."
      : isAr
        ? "نتيجة هذه الأداة استرشادية لمساعدتك على توضيح خطواتك التالية. لا نرسل أي رسالة خارجية تلقائياً، وكل إجراء يتطلب موافقة بشرية."
        : "This tool's result is indicative to help you clarify your next steps. We never auto-send any external message, and every action requires human approval.";

  return (
    <p
      className="mt-6 rounded-lg border border-border/60 bg-muted/40 px-4 py-3 text-xs leading-relaxed text-muted-foreground"
      dir={isAr ? "rtl" : "ltr"}
    >
      {text}
    </p>
  );
}
