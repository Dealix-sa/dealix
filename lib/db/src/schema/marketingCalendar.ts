import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
  boolean,
  date,
} from "drizzle-orm/pg-core";

export const marketingCalendar = pgTable("marketing_calendar", {
  id: uuid("id").defaultRandom().primaryKey(),
  slotDate: date("slot_date").notNull(),
  channel: varchar("channel", { length: 32 }).notNull(),
  contentType: varchar("content_type", { length: 64 }).notNull().default("post"),
  title: varchar("title", { length: 255 }).notNull(),
  bodyAr: text("body_ar"),
  bodyEn: text("body_en"),
  status: varchar("status", { length: 32 }).notNull().default("planned"),
  utm: jsonb("utm").$type<Record<string, string>>().notNull().default({}),
  isPublished: boolean("is_published").notNull().default(false),
  publishedAt: timestamp("published_at", { withTimezone: true }),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type MarketingSlot = typeof marketingCalendar.$inferSelect;
export type NewMarketingSlot = typeof marketingCalendar.$inferInsert;
