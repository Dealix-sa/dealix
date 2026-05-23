import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
} from "drizzle-orm/pg-core";

export const knowledgeBase = pgTable("knowledge_base", {
  id: uuid("id").defaultRandom().primaryKey(),
  slug: varchar("slug", { length: 128 }).notNull().unique(),
  titleAr: varchar("title_ar", { length: 255 }).notNull(),
  titleEn: varchar("title_en", { length: 255 }),
  bodyAr: text("body_ar").notNull(),
  bodyEn: text("body_en"),
  category: varchar("category", { length: 64 }).notNull().default("general"),
  tags: jsonb("tags").$type<string[]>().notNull().default([]),
  keywords: jsonb("keywords").$type<string[]>().notNull().default([]),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type KnowledgeArticle = typeof knowledgeBase.$inferSelect;
export type NewKnowledgeArticle = typeof knowledgeBase.$inferInsert;
