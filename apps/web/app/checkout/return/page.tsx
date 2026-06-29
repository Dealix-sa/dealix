import type { Metadata } from "next";
import { Suspense } from "react";
import CheckoutReturnClient from "./CheckoutReturnClient";

export const metadata: Metadata = {
  title: "تأكيد الدفع — Dealix",
  description: "حالة الدفع بعد إتمام العملية عبر مزوّد الدفع.",
  robots: { index: false, follow: false },
};

function Fallback() {
  return (
    <main style={{ maxWidth: 640, margin: "0 auto", padding: "64px 24px" }}>
      <section className="card" style={{ textAlign: "center" }}>
        <p className="eyebrow">Dealix · الدفع</p>
        <h1>جارٍ التحميل…</h1>
      </section>
    </main>
  );
}

export default function CheckoutReturnPage() {
  return (
    <Suspense fallback={<Fallback />}>
      <CheckoutReturnClient />
    </Suspense>
  );
}
