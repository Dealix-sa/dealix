import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
} from "drizzle-orm/pg-core";

export const evidenceEvents = pgTable("evidence_events", {
  id: uuid("id").defaultRandom().primaryKey(),
  eventType: varchar("event_type", { length: 64 }).notNull(),
  company: varchar("company", { length: 255 }).notNull(),
  motion: varchar("motion", { length: 64 }),
  offerId: varchar("offer_id", { length: 64 }),
  notes: text("notes"),
  payload: jsonb("payload").$type<Record<string, unknown>>().notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export type EvidenceEvent = typeof evidenceEvents.$inferSelect;
export type NewEvidenceEvent = typeof evidenceEvents.$inferInsert;
