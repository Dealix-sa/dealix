import { getDb, auditLog, type NewAuditLogEntry } from "@workspace/db";
import { desc, eq } from "drizzle-orm";

export async function writeAuditLog(entry: NewAuditLogEntry) {
  const db = getDb();
  await db.insert(auditLog).values(entry);
}

export async function listAuditLog(limit = 100) {
  const db = getDb();
  return db.select().from(auditLog).orderBy(desc(auditLog.createdAt)).limit(limit);
}

export async function getAuditLogForApproval(approvalId: string) {
  const db = getDb();
  return db
    .select()
    .from(auditLog)
    .where(eq(auditLog.approvalId, approvalId))
    .orderBy(desc(auditLog.createdAt));
}
