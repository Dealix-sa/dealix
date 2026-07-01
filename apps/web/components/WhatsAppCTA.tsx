"use client";

import { waLink, mailtoLink } from "@/lib/contact";

interface WhatsAppCTAProps {
  message: string;
  label?: string;
  fallbackSubject?: string;
  className?: string;
}

// WhatsApp deep link when NEXT_PUBLIC_WHATSAPP_NUMBER is configured,
// otherwise a mailto fallback — the CTA always renders something.
export default function WhatsAppCTA({
  message,
  label = "راسلنا على واتساب",
  fallbackSubject,
  className = "rounded-2xl bg-emerald-500 px-6 py-3 text-center text-sm font-bold text-white hover:bg-emerald-400",
}: WhatsAppCTAProps) {
  const wa = waLink(message);

  if (wa) {
    return (
      <a href={wa} target="_blank" rel="noopener noreferrer" className={className}>
        {label}
      </a>
    );
  }

  return (
    <a href={mailtoLink(fallbackSubject ?? label, message)} className={className}>
      {label.includes("واتساب") ? label.replace("واتساب", "البريد") : label}
    </a>
  );
}
