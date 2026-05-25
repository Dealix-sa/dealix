import type { Request, Response, NextFunction } from "express";
import { env, isDev } from "../env.js";
import { forbidden } from "../lib/errors.js";

export function requireInternalToken(
  req: Request,
  _res: Response,
  next: NextFunction,
) {
  const expected = env.DEALIX_INTERNAL_TOKEN;

  if (!expected) {
    if (isDev) return next();
    return next(forbidden("Internal token not configured on server"));
  }

  const provided =
    (req.headers["x-dealix-internal-token"] as string | undefined) ||
    (req.headers["X-Dealix-Internal-Token"] as unknown as string | undefined);

  if (!provided || provided !== expected) {
    return next(forbidden("Invalid or missing X-Dealix-Internal-Token header"));
  }
  next();
}
