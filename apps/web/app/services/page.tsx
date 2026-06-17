import type { Metadata } from "next";
import ServicesView from "../../components/ServicesView";

export const metadata: Metadata = {
  title: "Services — Governed AI Revenue for Saudi B2B",
  description:
    "Dealix services: free diagnostic, 499 SAR Revenue Proof Sprint, Data-to-Revenue Pack, monthly Growth Ops, Executive Command Center, and the founder-led Command Sprint. Approval-first, PDPL-aware.",
  alternates: { canonical: "/services", languages: { "ar-SA": "/ar/services", "en-US": "/services" } },
};

export default function ServicesPage() {
  return <ServicesView locale="en" />;
}
