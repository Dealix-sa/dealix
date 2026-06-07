import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Dealix — الأسعار والاشتراكات";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function OgImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          background: "#001F3F",
          position: "relative",
        }}
      >
        <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 8, background: "#D4AF37", display: "flex" }} />

        <div style={{ color: "#FFFFFF", fontSize: 54, fontWeight: 700, textAlign: "center", marginBottom: 12, direction: "rtl", display: "flex" }}>
          الأسعار والاشتراكات
        </div>
        <div style={{ color: "#D4AF37", fontSize: 28, fontWeight: 600, textAlign: "center", marginBottom: 40, display: "flex" }}>
          Pricing & Plans · سلم العروض
        </div>

        {/* Three tiers */}
        <div style={{ display: "flex", gap: 32, marginBottom: 32 }}>
          {[
            { label: "Sprint", price: "499 ريال", note: "لمرة واحدة" },
            { label: "Managed Ops", price: "2,999+", note: "شهرياً" },
            { label: "Enterprise AI", price: "مخصص", note: "Custom" },
          ].map((t) => (
            <div
              key={t.label}
              style={{
                background: "rgba(212,175,55,0.1)",
                border: "1px solid rgba(212,175,55,0.4)",
                borderRadius: 12,
                padding: "20px 28px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                minWidth: 240,
              }}
            >
              <div style={{ color: "#D4AF37", fontSize: 18, fontWeight: 700, marginBottom: 8, display: "flex" }}>{t.label}</div>
              <div style={{ color: "#FFFFFF", fontSize: 30, fontWeight: 700, marginBottom: 4, display: "flex" }}>{t.price}</div>
              <div style={{ color: "#FFFFFF", fontSize: 14, opacity: 0.6, display: "flex" }}>{t.note}</div>
            </div>
          ))}
        </div>

        <div style={{ color: "#FFFFFF", fontSize: 18, opacity: 0.65, display: "flex" }}>
          كل خطة تبني على الإثبات · Every plan builds on proof
        </div>

        <div style={{ position: "absolute", bottom: 28, right: 40, color: "#D4AF37", fontSize: 20, opacity: 0.7, display: "flex" }}>
          dealix.me/ar/pricing
        </div>
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 8, background: "#D4AF37", display: "flex" }} />
      </div>
    ),
    { ...size }
  );
}
