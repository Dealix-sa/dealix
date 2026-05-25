import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  integer,
  jsonb,
  numeric,
} from "drizzle-orm/pg-core";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";
import { leads } from "./leads.js";

export const deals = pgTable("deals", {
  id: uuid("id").defaultRandom().primaryKey(),
  leadId: uuid("lead_id").references(() => leads.id, { onDelete: "set null" }),
  title: varchar("title", { length: 255 }).notNull(),
  company: varchar("company", { length: 255 }).notNull(),
  value: numeric("value", { precision: 14, scale: 2 }).notNull().default("0"),
  currency: varchar("currency", { length: 8 }).notNull().default("SAR"),
  stage: varchar("stage", { length: 32 }).notNull().default("lead"),
  probability: integer("probability").notNull().default(20),
  aiScore: integer("ai_score").notNull().default(50),
  assignedTo: varchar("assigned_to", { length: 255 }),
  closeDate: timestamp("close_date", { withTimezone: true }),
  lastActivityAt: timestamp("last_activity_at", { withTimezone: true }).notNull().defaultNow(),
  tags: jsonb("tags").$type<string[]>().notNull().default([]),
  notes: text("notes"),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Deal = typeof deals.$inferSelect;
export type NewDeal = typeof deals.$inferInsert;

export const insertDealSchema = createInsertSchema(deals);
export const selectDealSchema = createSelectSchema(deals);
