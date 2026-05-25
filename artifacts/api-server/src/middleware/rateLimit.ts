import rateLimit from "express-rate-limit";
import { env } from "../env.js";

export const publicRateLimit = rateLimit({
  windowMs: 60_000,
  max: env.RATE_LIMIT_PUBLIC,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: "Too many requests",
    code: "rate_limited",
    retryAfterSeconds: 60,
  },
});

export const internalRateLimit = rateLimit({
  windowMs: 60_000,
  max: env.RATE_LIMIT_INTERNAL,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: "Too many requests",
    code: "rate_limited",
    retryAfterSeconds: 60,
  },
});

export const authRateLimit = rateLimit({
  windowMs: 15 * 60_000,
  max: 20,
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    error: "Too many auth attempts",
    code: "rate_limited",
    retryAfterSeconds: 900,
  },
});
