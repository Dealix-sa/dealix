import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
} from "drizzle-orm/pg-core";
import { createInsertSchema, createSelectSchema } from "drizzle-zod";

export const approvals = pgTable("approvals", {
  id: uuid("id").defaultRandom().primaryKey(),
  agentType: varchar("agent_type", { length: 64 }).notNull(),
  action: varchar("action", { length: 128 }).notNull(),
  description: text("description").notNull(),
  target: varchar("target", { length: 255 }).notNull(),
  riskLevel: varchar("risk_level", { length: 16 }).notNull().default("medium"),
  policyClass: varchar("policy_class", { length: 8 }).notNull().default("A2"),
  status: varchar("status", { length: 16 }).notNull().default("pending"),
  estimatedImpact: text("estimated_impact"),
  metadata: jsonb("metadata").$type<Record<string, unknown>>().notNull().default({}),
  requestedAt: timestamp("requested_at", { withTimezone: true }).notNull().defaultNow(),
  reviewedAt: timestamp("reviewed_at", { withTimezone: true }),
  reviewedBy: varchar("reviewed_by", { length: 255 }),
  rejectionReason: text("rejection_reason"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export type Approval = typeof approvals.$inferSelect;
export type NewApproval = typeof approvals.$inferInsert;

export const insertApprovalSchema = createInsertSchema(approvals);
export const selectApprovalSchema = createSelectSchema(approvals);
