import type { Request, Response, NextFunction } from "express";
import { verifyToken } from "../lib/jwt.js";
import { unauthorized } from "../lib/errors.js";

export function requireAuth(req: Request, _res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) {
    return next(unauthorized("Missing Bearer token"));
  }
  const token = header.slice(7).trim();
  try {
    const payload = verifyToken(token);
    if (payload.type !== "access") {
      return next(unauthorized("Wrong token type"));
    }
    req.user = payload;
    next();
  } catch {
    next(unauthorized("Invalid or expired token"));
  }
}

export function optionalAuth(req: Request, _res: Response, next: NextFunction) {
  const header = req.headers.authorization;
  if (!header || !header.startsWith("Bearer ")) return next();
  try {
    const payload = verifyToken(header.slice(7).trim());
    if (payload.type === "access") req.user = payload;
  } catch {
    /* ignore */
  }
  next();
}
