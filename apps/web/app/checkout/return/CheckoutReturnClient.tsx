"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";

const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? "https://api.dealix.me";

type Status = {
  state: "paid" | "pending" | "failed";
  paid: boolean;
  amount_sar: number | null;
  plan: string | null;
  reference: string;
};

const MAX_POLLS = 8;
const POLL_MS = 3000;

export default function CheckoutReturnClient() {
  const params = useSearchParams();
  // Moyasar redirects with ?id=<payment_id>&status=<...>
  const paymentId = params.get("id") ?? params.get("payment_id") ?? "";
  const hintedStatus = params.get("status") ?? "";

  const [status, setStatus] = useState<Status | null>(null);
  const [polls, setPolls] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (!paymentId) {
      setDone(true);
      return;
    }
    let cancelled = false;

    async function check(attempt: number) {
      try {
        const res = await fetch(
          `${apiUrl}/api/v1/checkout/status?payment_id=${encodeURIComponent(paymentId)}`,
          { cache: "no-store" }
        );
        const data: Status = await res.json();
        if (cancelled) return;
        setStatus(data);
        if (data.state !== "pending" || attempt + 1 >= MAX_POLLS) {
          setDone(true);
          return;
        }
      } catch {
        if (cancelled) return;
        if (attempt + 1 >= MAX_POLLS) {
          setDone(true);
          return;
        }
      }
      setPolls(attempt + 1);
      setTimeout(() => check(attempt + 1), POLL_MS);
    }

    check(0);
    return () => {
      cancelled = true;
    };
  }, [paymentId]);

  // Resolve the display state: confirmed status > URL hint > pending.
  const state: "paid" | "pending" | "failed" =
    status?.state ?? (hintedStatus === "paid" ? "paid" : "pending");
  const settling = !done && state === "pending";

  return (
    <main style={{ maxWidth: 640, margin: "0 auto", padding: "64px 24px" }}>
      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Dealix · الدفع</p>

        {state === "paid" && (
          <>
            <div style={{ fontSize: "3rem", marginBottom: 8 }}>✅</div>
            <h1>تم استلام دفعتك بنجاح</h1>
            <p style={{ maxWidth: 460, margin: "12px auto" }}>
              شكراً لك. سيتواصل معك فريق Dealix خلال 24 ساعة لبدء البرنامج.
            </p>
            <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.55)" }}>
              Payment received — the Dealix team will contact you within 24 hours
              to begin your program.
            </p>
            {status?.amount_sar ? (
              <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 20, flexWrap: "wrap" }}>
                <span className="badge badge-emerald">
                  {status.amount_sar.toLocaleString("en-US")} ر.س
                </span>
                {status.plan ? <span className="badge badge-gold">{status.plan}</span> : null}
              </div>
            ) : null}
          </>
        )}

        {settling && (
          <>
            <div style={{ fontSize: "3rem", marginBottom: 8 }}>⏳</div>
            <h1>جارٍ تأكيد الدفع…</h1>
            <p style={{ maxWidth: 460, margin: "12px auto" }}>
              نتحقق من حالة الدفع لدى مزوّد الدفع. لا تغلق هذه الصفحة.
            </p>
            <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.55)" }}>
              Confirming your payment with the provider — please don’t close this page.
            </p>
          </>
        )}

        {done && state === "pending" && (
          <>
            <div style={{ fontSize: "3rem", marginBottom: 8 }}>🔎</div>
            <h1>لم نؤكد الدفع بعد</h1>
            <p style={{ maxWidth: 460, margin: "12px auto" }}>
              إن كنت قد أتممت الدفع، فقد يستغرق التأكيد بضع دقائق. احتفظ برقم المرجع
              أدناه وسنتابع معك.
            </p>
            <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.55)" }}>
              If you completed payment, confirmation may take a few minutes. Keep the
              reference below — we’ll follow up.
            </p>
          </>
        )}

        {state === "failed" && (
          <>
            <div style={{ fontSize: "3rem", marginBottom: 8 }}>⚠️</div>
            <h1>لم تكتمل عملية الدفع</h1>
            <p style={{ maxWidth: 460, margin: "12px auto" }}>
              لم نستلم دفعة مؤكدة. يمكنك المحاولة مرة أخرى أو التواصل معنا للمساعدة.
            </p>
            <p style={{ fontSize: "0.85rem", color: "rgba(255,255,255,0.55)" }}>
              We didn’t receive a confirmed payment. You can try again or contact us.
            </p>
          </>
        )}

        {paymentId ? (
          <p style={{ fontSize: "0.75rem", color: "rgba(255,255,255,0.4)", marginTop: 24 }}>
            رقم المرجع / Reference: <code>{paymentId}</code>
          </p>
        ) : (
          <p style={{ fontSize: "0.8rem", color: "rgba(255,255,255,0.5)", marginTop: 24 }}>
            لا يوجد رقم مرجع في الرابط. / No payment reference in the link.
          </p>
        )}

        <div style={{ display: "flex", gap: 12, justifyContent: "center", marginTop: 28, flexWrap: "wrap" }}>
          <a href="/ar" className="badge badge-gold" style={{ textDecoration: "none" }}>
            العودة للرئيسية ←
          </a>
          {state === "failed" ? (
            <a href="/ar/pricing" className="badge badge-emerald" style={{ textDecoration: "none" }}>
              عرض الباقات
            </a>
          ) : null}
        </div>
      </section>
    </main>
  );
}
