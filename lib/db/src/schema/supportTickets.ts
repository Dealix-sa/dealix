import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
} from "drizzle-orm/pg-core";

export const supportTickets = pgTable("support_tickets", {
  id: uuid("id").defaultRandom().primaryKey(),
  subject: varchar("subject", { length: 255 }).notNull(),
  body: text("body").notNull(),
  customerEmail: varchar("customer_email", { length: 255 }),
  customerName: varchar("customer_name", { length: 255 }),
  company: varchar("company", { length: 255 }),
  category: varchar("category", { length: 64 }).notNull().default("general"),
  priority: varchar("priority", { length: 16 }).notNull().default("normal"),
  status: varchar("status", { length: 32 }).notNull().default("open"),
  sentiment: varchar("sentiment", { length: 16 }),
  aiClassification: jsonb("ai_classification").$type<Record<string, unknown>>().default({}),
  aiDraftResponse: text("ai_draft_response"),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type SupportTicket = typeof supportTickets.$inferSelect;
export type NewSupportTicket = typeof supportTickets.$inferInsert;
