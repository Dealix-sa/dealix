import {
  pgTable,
  text,
  timestamp,
  uuid,
  varchar,
  jsonb,
  boolean,
} from "drizzle-orm/pg-core";

export const auditLog = pgTable("audit_log", {
  id: uuid("id").defaultRandom().primaryKey(),
  approvalId: uuid("approval_id"),
  actor: varchar("actor", { length: 255 }).notNull(),
  decision: varchar("decision", { length: 32 }).notNull(),
  policyResult: jsonb("policy_result").$type<Record<string, unknown>>().notNull().default({}),
  externalActionAllowed: boolean("external_action_allowed").notNull().default(false),
  riskLevel: varchar("risk_level", { length: 16 }).notNull().default("medium"),
  evidence: jsonb("evidence").$type<Record<string, unknown>>().notNull().default({}),
  reason: text("reason"),
  ipAddress: varchar("ip_address", { length: 64 }),
  userAgent: text("user_agent"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export type AuditLogEntry = typeof auditLog.$inferSelect;
export type NewAuditLogEntry = typeof auditLog.$inferInsert;
