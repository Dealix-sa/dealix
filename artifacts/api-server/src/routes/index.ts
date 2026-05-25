import { Router } from "express";
import { healthRouter } from "./health.js";
import { authRouter } from "./v1/auth.js";
import { dashboardRouter } from "./v1/dashboard.js";
import { pipelineRouter } from "./v1/pipeline.js";
import { aiWorkforceRouter } from "./v1/aiWorkforce.js";
import { approvalsRouter } from "./v1/approvals.js";
import { publicRouter } from "./v1/publicRoutes.js";
import { businessNowRouter } from "./v1/businessNow.js";
import { businessRouter } from "./v1/business.js";
import { transformationRouter } from "./v1/transformation.js";
import { miscRouter } from "./v1/misc.js";
import { warRoomRouter } from "./v1/opsAutopilot/warRoom.js";
import { targetingRouter } from "./v1/opsAutopilot/targeting.js";
import { marketingRouter } from "./v1/opsAutopilot/marketing.js";
import {
  salesRouter,
  evidenceRouter,
  founderEvidenceRouter,
  opsLeadsRouter,
} from "./v1/opsAutopilot/salesEvidence.js";
import {
  supportRouter,
  knowledgeAdminRouter,
  invoicesRouter,
} from "./v1/opsAutopilot/support.js";
import {
  founderRouter,
  founderDashboardRouter,
} from "./v1/opsAutopilot/founder.js";
import { internalRouter } from "./v1/internal.js";
import { publicRateLimit, internalRateLimit } from "../middleware/rateLimit.js";

export function buildRouter(): Router {
  const root = Router();

  root.use(healthRouter);

  const v1 = Router();

  v1.use("/auth", authRouter);
  v1.use("/dashboard", dashboardRouter);
  v1.use("/revenue-pipeline", pipelineRouter);
  v1.use("/ai-workforce", aiWorkforceRouter);
  v1.use("/approvals", approvalsRouter);

  v1.use("/public", publicRateLimit, publicRouter);
  v1.use("/pricing", publicRouter);

  v1.use("/business-now", businessNowRouter);
  v1.use("/business", businessRouter);
  v1.use("/transformation", transformationRouter);
  v1.use(miscRouter);

  v1.use("/ops-autopilot/war-room", warRoomRouter);
  v1.use("/ops-autopilot/targeting", targetingRouter);
  v1.use("/ops-autopilot/marketing", marketingRouter);
  v1.use("/sales", salesRouter);
  v1.use("/evidence", evidenceRouter);
  v1.use("/ops-autopilot/founder/evidence", founderEvidenceRouter);
  v1.use("/ops-autopilot/leads", opsLeadsRouter);
  v1.use("/support", supportRouter);
  v1.use("/knowledge", knowledgeAdminRouter);
  v1.use("/invoices", invoicesRouter);
  v1.use("/ops-autopilot/founder", founderRouter);
  v1.use("/ops-autopilot/founder-dashboard", founderDashboardRouter);

  v1.use("/internal", internalRateLimit, internalRouter);

  root.use("/api/v1", v1);

  return root;
}
