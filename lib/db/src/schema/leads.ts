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
import { z } from "zod";

export const leads = pgTable("leads", {
  id: uuid("id").defaultRandom().primaryKey(),
  company: varchar("company", { length: 255 }).notNull(),
  contactName: varchar("contact_name", { length: 255 }),
  contactEmail: varchar("contact_email", { length: 255 }),
  contactPhone: varchar("contact_phone", { length: 64 }),
  industry: varchar("industry", { length: 128 }),
  city: varchar("city", { length: 128 }),
  country: varchar("country", { length: 64 }).notNull().default("SA"),
  source: varchar("source", { length: 64 }).notNull().default("inbound"),
  stage: varchar("stage", { length: 32 }).notNull().default("lead"),
  status: varchar("status", { length: 32 }).notNull().default("new"),
  priority: varchar("priority", { length: 16 }).notNull().default("p1"),
  estimatedValue: numeric("estimated_value", { precision: 14, scale: 2 }).notNull().default("0"),
  currency: varchar("currency", { length: 8 }).notNull().default("SAR"),
  aiScore: integer("ai_score").notNull().default(50),
  riskScore: integer("risk_score").notNull().default(0),
  engagementScore: integer("engagement_score").notNull().default(0),
  notes: text("notes"),
  tags: jsonb("tags").$type<string[]>().notNull().default([]),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  lastContactedAt: timestamp("last_contacted_at", { withTimezone: true }),
  nextFollowUpAt: timestamp("next_follow_up_at", { withTimezone: true }),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Lead = typeof leads.$inferSelect;
export type NewLead = typeof leads.$inferInsert;

export const insertLeadSchema = createInsertSchema(leads, {
  contactEmail: z.string().email().optional(),
  estimatedValue: z.union([z.string(), z.number()]).optional(),
});

export const selectLeadSchema = createSelectSchema(leads);

export const publicLeadSchema = z.object({
  company: z.string().min(1),
  contactName: z.string().optional(),
  contactEmail: z.string().email().optional(),
  contactPhone: z.string().optional(),
  industry: z.string().optional(),
  city: z.string().optional(),
  notes: z.string().optional(),
  source: z.string().optional(),
});
