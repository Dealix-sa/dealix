import "dotenv/config";

function bool(v: string | undefined, fallback = false): boolean {
  if (v == null) return fallback;
  return ["1", "true", "yes", "on"].includes(v.toLowerCase());
}

export const env = {
  NODE_ENV: process.env.NODE_ENV || "development",
  PORT: parseInt(process.env.PORT || "8000", 10),
  HOST: process.env.HOST || "0.0.0.0",

  DATABASE_URL:
    process.env.DATABASE_URL ||
    "postgresql://postgres:postgres@localhost:5432/dealix",

  JWT_SECRET:
    process.env.JWT_SECRET ||
    "dev-only-jwt-secret-change-in-production-must-be-at-least-32-chars",
  JWT_ACCESS_TTL_SECONDS: parseInt(
    process.env.JWT_ACCESS_TTL_SECONDS || "900",
    10,
  ), // 15 min
  JWT_REFRESH_TTL_SECONDS: parseInt(
    process.env.JWT_REFRESH_TTL_SECONDS || "604800",
    10,
  ), // 7 days

  DEALIX_ADMIN_API_KEY: process.env.DEALIX_ADMIN_API_KEY || "",
  DEALIX_INTERNAL_TOKEN: process.env.DEALIX_INTERNAL_TOKEN || "",

  OPENAI_API_KEY: process.env.OPENAI_API_KEY || "",
  OPENAI_MODEL: process.env.OPENAI_MODEL || "gpt-4o-mini",
  OPENAI_BASE_URL: process.env.OPENAI_BASE_URL || "https://api.openai.com/v1",
  ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY || "",
  ANTHROPIC_MODEL: process.env.ANTHROPIC_MODEL || "claude-sonnet-4-6",

  CORS_ORIGINS: (
    process.env.CORS_ORIGINS ||
    "http://localhost:3000,http://localhost:3100"
  )
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean),

  RATE_LIMIT_PUBLIC: parseInt(process.env.RATE_LIMIT_PUBLIC || "100", 10),
  RATE_LIMIT_INTERNAL: parseInt(process.env.RATE_LIMIT_INTERNAL || "500", 10),

  WS_HEARTBEAT_MS: parseInt(process.env.WS_HEARTBEAT_MS || "7000", 10),
  WORKER_STALE_MINUTES: parseInt(
    process.env.WORKER_STALE_MINUTES || "30",
    10,
  ),

  DISABLE_DB: bool(process.env.DISABLE_DB, false),
  ENABLE_REQUEST_LOG: bool(process.env.ENABLE_REQUEST_LOG, true),
} as const;

export const isProd = env.NODE_ENV === "production";
export const isDev = env.NODE_ENV !== "production";
