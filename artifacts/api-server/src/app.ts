import express, { type Application } from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import { env, isProd } from "./env.js";
import { buildRouter } from "./routes/index.js";
import { errorHandler, notFoundHandler } from "./middleware/errorHandler.js";

export function createApp(): Application {
  const app = express();

  app.disable("x-powered-by");
  app.set("trust proxy", 1);

  app.use(
    helmet({
      contentSecurityPolicy: false,
      crossOriginResourcePolicy: { policy: "cross-origin" },
    }),
  );

  app.use(
    cors({
      origin(origin, cb) {
        if (!origin) return cb(null, true);
        if (env.CORS_ORIGINS.includes("*")) return cb(null, true);
        if (env.CORS_ORIGINS.includes(origin)) return cb(null, true);
        if (!isProd) return cb(null, true);
        return cb(null, false);
      },
      credentials: true,
      methods: ["GET", "POST", "PATCH", "DELETE", "PUT", "OPTIONS"],
      allowedHeaders: [
        "Content-Type",
        "Authorization",
        "X-Admin-API-Key",
        "X-Dealix-Internal-Token",
      ],
    }),
  );

  app.use(express.json({ limit: "1mb" }));
  app.use(express.urlencoded({ extended: false }));

  if (env.ENABLE_REQUEST_LOG && !isProd) {
    app.use(morgan("dev"));
  } else if (env.ENABLE_REQUEST_LOG) {
    app.use(morgan("combined"));
  }

  app.use(buildRouter());

  app.get("/", (_req, res) => {
    res.json({
      service: "Dealix API",
      version: "5.0.0",
      status: "ok",
      docs: "/api/v1",
      health: "/healthz",
      timestamp: new Date().toISOString(),
    });
  });

  app.use(notFoundHandler);
  app.use(errorHandler);

  return app;
}
