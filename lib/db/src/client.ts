import { drizzle, type NodePgDatabase } from "drizzle-orm/node-postgres";
import pg from "pg";
import * as schema from "./schema/index.js";

const { Pool } = pg;

let _pool: pg.Pool | null = null;
let _db: NodePgDatabase<typeof schema> | null = null;

export function getPool(): pg.Pool {
  if (_pool) return _pool;
  const url = process.env.DATABASE_URL;
  if (!url) {
    throw new Error(
      "DATABASE_URL is not set. Set it to a valid PostgreSQL connection string before connecting.",
    );
  }
  _pool = new Pool({
    connectionString: url,
    max: parseInt(process.env.PG_POOL_MAX || "10", 10),
    idleTimeoutMillis: 30_000,
    ssl: url.includes("sslmode=require") || /\.(supabase|render|railway)\./.test(url)
      ? { rejectUnauthorized: false }
      : undefined,
  });
  return _pool;
}

export function getDb(): NodePgDatabase<typeof schema> {
  if (_db) return _db;
  _db = drizzle(getPool(), { schema });
  return _db;
}

export type DB = NodePgDatabase<typeof schema>;
export { schema };
