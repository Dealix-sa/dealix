import type { Request, Response, NextFunction } from "express";
import { env, isDev } from "../env.js";
import { forbidden } from "../lib/errors.js";

export function requireAdminKey(
  req: Request,
  _res: Response,
  next: NextFunction,
) {
  const expected = env.DEALIX_ADMIN_API_KEY;

  if (!expected) {
    if (isDev) return next();
    return next(forbidden("Admin API key not configured on server"));
  }

  const provided =
    (req.headers["x-admin-api-key"] as string | undefined) ||
    (req.headers["X-Admin-API-Key"] as unknown as string | undefined) ||
    (req.query.admin_key as string | undefined);

  if (!provided || provided !== expected) {
    return next(forbidden("Invalid or missing X-Admin-API-Key header"));
  }
  next();
}
