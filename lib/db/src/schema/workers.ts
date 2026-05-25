import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  integer,
  jsonb,
} from "drizzle-orm/pg-core";

export const workers = pgTable("workers", {
  id: uuid("id").defaultRandom().primaryKey(),
  name: varchar("name", { length: 128 }).notNull().unique(),
  type: varchar("type", { length: 64 }).notNull().default("agent"),
  status: varchar("status", { length: 16 }).notNull().default("idle"),
  lastRunAt: timestamp("last_run_at", { withTimezone: true }),
  lastSuccessAt: timestamp("last_success_at", { withTimezone: true }),
  lastErrorAt: timestamp("last_error_at", { withTimezone: true }),
  lastError: text("last_error"),
  runCount: integer("run_count").notNull().default(0),
  successCount: integer("success_count").notNull().default(0),
  failureCount: integer("failure_count").notNull().default(0),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Worker = typeof workers.$inferSelect;
export type NewWorker = typeof workers.$inferInsert;
