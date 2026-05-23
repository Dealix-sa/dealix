import type { Request, Response, NextFunction } from "express";
import { HttpError } from "../lib/errors.js";
import { isProd } from "../env.js";

export function notFoundHandler(req: Request, res: Response) {
  res.status(404).json({
    error: "not_found",
    code: "not_found",
    message: `Route ${req.method} ${req.path} not found`,
  });
}

export function errorHandler(
  err: unknown,
  _req: Request,
  res: Response,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  _next: NextFunction,
) {
  if (err instanceof HttpError) {
    res.status(err.status).json({
      error: err.message,
      code: err.code,
      details: err.details,
    });
    return;
  }

  const e = err as Error;
  if (!isProd) {
    // eslint-disable-next-line no-console
    console.error("[error]", e);
  }
  res.status(500).json({
    error: "internal_error",
    code: "internal_error",
    message: isProd ? "Internal server error" : e?.message || "Unknown error",
  });
}
