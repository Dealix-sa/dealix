import { ImageResponse } from "next/og";

/**
 * Root-level OpenGraph image for Dealix. Next.js renders this at the edge as
 * a real 1200x630 PNG, so social media (LinkedIn, X, WhatsApp) gets a proper
 * preview without us shipping a binary asset in the repo.
 *
 * Brand colors per docs/sales-kit/dealix_brand_guidelines.md:
 *   Deep Green #0A4D3F   Gold #C9A961   Sand #F4F0E8
 */
export const runtime = "edge";
export const alt = "Dealix — Post-Lead Revenue OS";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function OG() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          padding: "80px",
          background:
            "linear-gradient(135deg, #0A4D3F 0%, #0A4D3F 60%, #0D5F4D 100%)",
          color: "#F4F0E8",
          fontFamily: "system-ui, -apple-system, sans-serif",
        }}
      >
        {/* Top: mark + brand line */}
        <div style={{ display: "flex", alignItems: "center", gap: 24 }}>
          <div
            style={{
              width: 72,
              height: 72,
              borderRadius: 16,
              background: "#F4F0E8",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 48,
              fontWeight: 700,
              color: "#0A4D3F",
            }}
          >
            D
          </div>
          <div style={{ display: "flex", flexDirection: "column" }}>
            <span style={{ fontSize: 36, fontWeight: 700, letterSpacing: -1 }}>
              Dealix
            </span>
            <span style={{ fontSize: 18, color: "#C9A961", letterSpacing: 1 }}>
              POST-LEAD REVENUE OS
            </span>
          </div>
        </div>

        {/* Gold accent line */}
        <div
          style={{
            marginTop: 56,
            width: 96,
            height: 4,
            background: "#C9A961",
            display: "flex",
          }}
        />

        {/* Headline */}
        <div
          style={{
            marginTop: 32,
            fontSize: 64,
            fontWeight: 700,
            lineHeight: 1.15,
            maxWidth: 980,
            display: "flex",
          }}
        >
          Proves what happens after the lead.
        </div>

        {/* Sub-headline */}
        <div
          style={{
            marginTop: 28,
            fontSize: 24,
            color: "#F4F0E8",
            opacity: 0.85,
            maxWidth: 880,
            lineHeight: 1.4,
            display: "flex",
          }}
        >
          Owner · Approval · Evidence · Next Action. Governed for Saudi B2B.
        </div>

        {/* Footer pill */}
        <div
          style={{
            marginTop: "auto",
            display: "flex",
            alignItems: "center",
            gap: 16,
            fontSize: 18,
            color: "#F4F0E8",
            opacity: 0.7,
          }}
        >
          <span>PDPL-aligned</span>
          <span>·</span>
          <span>No cold WhatsApp</span>
          <span>·</span>
          <span>No LinkedIn automation</span>
        </div>
      </div>
    ),
    { ...size },
  );
}
