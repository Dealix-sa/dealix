import { Router } from "express";
import { getPool } from "@workspace/db";

export const healthRouter = Router();

healthRouter.get("/healthz", async (_req, res) => {
  let dbOk = false;
  let dbError: string | undefined;
  try {
    const pool = getPool();
    await pool.query("SELECT 1");
    dbOk = true;
  } catch (e) {
    dbError = (e as Error).message;
  }
  res.json({
    status: "ok",
    service: "dealix-api-server",
    version: "5.0.0",
    timestamp: new Date().toISOString(),
    db: dbOk ? "ok" : "down",
    dbError: dbError && process.env.NODE_ENV !== "production" ? dbError : undefined,
  });
});

healthRouter.get("/health", (_req, res) =>
  res.json({ status: "ok", timestamp: new Date().toISOString() }),
);

healthRouter.get("/api/healthz", (_req, res) =>
  res.json({
    status: "ok",
    service: "dealix-api-server",
    timestamp: new Date().toISOString(),
  }),
);
