import type { Request, Response, NextFunction } from "express";
import type { ZodSchema } from "zod";
import { badRequest } from "../lib/errors.js";

export function validateBody<T>(schema: ZodSchema<T>) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return next(badRequest("Invalid request body", result.error.format()));
    }
    req.body = result.data as Record<string, unknown>;
    next();
  };
}

export function validateQuery<T>(schema: ZodSchema<T>) {
  return (req: Request, _res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.query);
    if (!result.success) {
      return next(badRequest("Invalid query parameters", result.error.format()));
    }
    next();
  };
}
