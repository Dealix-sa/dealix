import { createServer } from "http";
import { createApp } from "./app.js";
import { env } from "./env.js";
import { wsHub } from "./lib/wsHub.js";

const app = createApp();
const server = createServer(app);
wsHub.attach(server);

server.listen(env.PORT, env.HOST, () => {
  // eslint-disable-next-line no-console
  console.log(
    `[dealix-api] listening on http://${env.HOST}:${env.PORT} (env=${env.NODE_ENV})`,
  );
});

const shutdown = (signal: string) => {
  // eslint-disable-next-line no-console
  console.log(`[dealix-api] received ${signal}, shutting down...`);
  wsHub.close();
  server.close(() => process.exit(0));
  setTimeout(() => process.exit(1), 5000).unref();
};
process.on("SIGTERM", () => shutdown("SIGTERM"));
process.on("SIGINT", () => shutdown("SIGINT"));
