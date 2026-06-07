import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Dealix — تشخيص 7 أيام بالأدلة";
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

        {/* Badge: Free */}
        <div
          style={{
            background: "#D4AF37",
            color: "#001F3F",
            fontSize: 18,
            fontWeight: 700,
            padding: "8px 24px",
            borderRadius: 24,
            marginBottom: 28,
            letterSpacing: 1,
            display: "flex",
          }}
        >
          مجاني · FREE
        </div>

        <div style={{ color: "#FFFFFF", fontSize: 56, fontWeight: 700, textAlign: "center", marginBottom: 16, direction: "rtl", display: "flex" }}>
          تشخيص ٧ أيام بالأدلة
        </div>
        <div style={{ color: "#D4AF37", fontSize: 30, fontWeight: 600, textAlign: "center", marginBottom: 36, display: "flex" }}>
          7-Day Evidence-Governed Diagnostic
        </div>

        <div style={{ display: "flex", gap: 32, color: "#FFFFFF", fontSize: 19, opacity: 0.8 }}>
          <span>✓ Proof Pack يوم 7</span>
          <span>·</span>
          <span>✓ PDPL أصيل</span>
          <span>·</span>
          <span>✓ استرجاع ١٤ يوم</span>
        </div>

        <div style={{ position: "absolute", bottom: 28, right: 40, color: "#D4AF37", fontSize: 20, opacity: 0.7, display: "flex" }}>
          dealix.me/ar/dealix-diagnostic
        </div>
        <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 8, background: "#D4AF37", display: "flex" }} />
      </div>
    ),
    { ...size }
  );
}
