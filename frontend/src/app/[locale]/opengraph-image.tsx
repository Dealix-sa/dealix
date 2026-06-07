import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Dealix — Saudi B2B Revenue Operating System";
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
        {/* Gold accent top bar */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: 8,
            background: "#D4AF37",
            display: "flex",
          }}
        />

        {/* Logo mark */}
        <div
          style={{
            width: 90,
            height: 90,
            background: "#001F3F",
            borderRadius: 14,
            border: "2px solid #D4AF37",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            marginBottom: 32,
          }}
        >
          <span style={{ color: "#D4AF37", fontSize: 52, fontWeight: 700 }}>D</span>
        </div>

        {/* Arabic headline */}
        <div
          style={{
            color: "#FFFFFF",
            fontSize: 52,
            fontWeight: 700,
            textAlign: "center",
            marginBottom: 16,
            direction: "rtl",
          }}
        >
          نظام تشغيل الإيرادات B2B السعودي
        </div>

        {/* English sub-headline */}
        <div
          style={{
            color: "#D4AF37",
            fontSize: 28,
            fontWeight: 600,
            textAlign: "center",
            letterSpacing: 2,
            marginBottom: 40,
          }}
        >
          DEALIX — SAUDI REVENUE OPERATING SYSTEM
        </div>

        {/* Three pillars */}
        <div
          style={{
            display: "flex",
            gap: 48,
            color: "#FFFFFF",
            fontSize: 20,
            opacity: 0.75,
          }}
        >
          <span>PDPL أصيل</span>
          <span style={{ color: "#D4AF37", opacity: 0.5 }}>·</span>
          <span>ZATCA جاهز</span>
          <span style={{ color: "#D4AF37", opacity: 0.5 }}>·</span>
          <span>موافقة أولاً</span>
        </div>

        {/* URL bottom right */}
        <div
          style={{
            position: "absolute",
            bottom: 28,
            right: 40,
            color: "#D4AF37",
            fontSize: 20,
            opacity: 0.7,
            display: "flex",
          }}
        >
          dealix.me
        </div>

        {/* Gold accent bottom bar */}
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: 8,
            background: "#D4AF37",
            display: "flex",
          }}
        />
      </div>
    ),
    { ...size }
  );
}
