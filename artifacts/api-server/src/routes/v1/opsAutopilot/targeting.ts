import { Router } from "express";
import { z } from "zod";
import { and, desc, eq } from "drizzle-orm";
import { getDb, leads } from "@workspace/db";
import { validateBody } from "../../../middleware/validate.js";
import { requireAdminKey } from "../../../middleware/requireAdminKey.js";
import { scoreLead } from "../../../lib/scoring.js";

export const targetingRouter = Router();
targetingRouter.use(requireAdminKey);

function publicTarget(l: typeof leads.$inferSelect) {
  return {
    id: l.id,
    company: l.company,
    contactName: l.contactName,
    industry: l.industry,
    city: l.city,
    priority: l.priority,
    aiScore: l.aiScore,
    estimatedValue: Number(l.estimatedValue),
    stage: l.stage,
    notes: l.notes,
  };
}

targetingRouter.get("/today", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 5), 10) || 5, 50);
    const db = getDb();
    const rows = await db
      .select()
      .from(leads)
      .where(eq(leads.priority, "p0"))
      .orderBy(desc(leads.aiScore))
      .limit(topN);
    res.json({
      targets: rows.map(publicTarget),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

targetingRouter.get("/pool", async (_req, res, next) => {
  try {
    const db = getDb();
    const rows = await db.select().from(leads).orderBy(desc(leads.aiScore)).limit(200);
    res.json({
      pool: rows.map(publicTarget),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

targetingRouter.get("/p0-today", async (req, res, next) => {
  try {
    const topN = Math.min(parseInt(String(req.query.top_n ?? 10), 10) || 10, 100);
    const db = getDb();
    const rows = await db
      .select()
      .from(leads)
      .where(and(eq(leads.priority, "p0"), eq(leads.status, "new"))!)
      .orderBy(desc(leads.aiScore))
      .limit(topN);
    res.json({
      targets: rows.map(publicTarget),
      total: rows.length,
      generatedAt: new Date().toISOString(),
    });
  } catch (e) {
    next(e);
  }
});

const importSchema = z.object({ csv_text: z.string().min(1) });

targetingRouter.post(
  "/import",
  validateBody(importSchema),
  async (req, res, next) => {
    try {
      const csv = (req.body as z.infer<typeof importSchema>).csv_text;
      const lines = csv.split(/\r?\n/).filter((l) => l.trim());
      if (lines.length < 2) {
        return res.json({ inserted: 0, errors: ["empty csv or missing header"] });
      }
      const header = lines[0]!.split(",").map((h) => h.trim().toLowerCase());
      const idx = (name: string) => header.indexOf(name);
      const db = getDb();
      let inserted = 0;
      for (let i = 1; i < lines.length; i++) {
        const cells = lines[i]!.split(",").map((c) => c.trim());
        const company = cells[idx("company")] || cells[0] || "";
        if (!company) continue;
        const industry = cells[idx("industry")] || cells[idx("sector")] || null;
        const email = cells[idx("email")] || null;
        const phone = cells[idx("phone")] || null;
        const value = parseFloat(cells[idx("value")] || cells[idx("estimated_value")] || "0") || 0;
        const aiScore = scoreLead({
          estimatedValue: value,
          industry,
          contactEmail: email,
          contactPhone: phone,
          source: "csv_targeting",
        });
        await db.insert(leads).values({
          company,
          contactEmail: email,
          contactPhone: phone,
          industry,
          estimatedValue: String(value),
          aiScore,
          priority: "p1",
          source: "csv_targeting",
        });
        inserted++;
      }
      res.json({ inserted, generatedAt: new Date().toISOString() });
    } catch (e) {
      next(e);
    }
  },
);
