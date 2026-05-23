import { Router } from "express";
import bcrypt from "bcryptjs";
import { z } from "zod";
import { eq, and } from "drizzle-orm";
import {
  getDb,
  users,
  sessions,
  loginSchema,
  registerSchema,
} from "@workspace/db";
import { signAccessToken, signRefreshToken, verifyToken } from "../../lib/jwt.js";
import { validateBody } from "../../middleware/validate.js";
import { requireAuth } from "../../middleware/requireAuth.js";
import { authRateLimit } from "../../middleware/rateLimit.js";
import { unauthorized, badRequest, conflict } from "../../lib/errors.js";

export const authRouter = Router();

function publicUser(u: typeof users.$inferSelect) {
  return {
    id: u.id,
    email: u.email,
    fullName: u.fullName,
    company: u.company,
    role: u.role as "admin" | "manager" | "analyst",
    avatar: u.avatar ?? undefined,
    createdAt: u.createdAt.toISOString(),
  };
}

async function issueTokens(user: typeof users.$inferSelect, req: { headers: Record<string, unknown>; ip?: string }) {
  const db = getDb();
  const access = signAccessToken({
    sub: user.id,
    email: user.email,
    role: user.role,
  });
  const refresh = signRefreshToken({
    sub: user.id,
    email: user.email,
    role: user.role,
  });
  await db.insert(sessions).values({
    userId: user.id,
    refreshToken: refresh.token,
    userAgent: (req.headers["user-agent"] as string | undefined) || null,
    ipAddress: req.ip || null,
    expiresAt: new Date(refresh.expiresAt),
  });
  return {
    accessToken: access.token,
    refreshToken: refresh.token,
    expiresAt: access.expiresAt,
  };
}

authRouter.post(
  "/register",
  authRateLimit,
  validateBody(registerSchema),
  async (req, res, next) => {
    try {
      const { email, password, fullName, company } = req.body as z.infer<
        typeof registerSchema
      >;
      const db = getDb();
      const existing = await db.select().from(users).where(eq(users.email, email)).limit(1);
      if (existing.length) throw conflict("Email already registered");
      const hash = await bcrypt.hash(password, 12);
      const role = email.endsWith("@dealix.ai") || email.endsWith("@dealix.sa") ? "admin" : "analyst";
      const [created] = await db
        .insert(users)
        .values({
          email,
          passwordHash: hash,
          fullName,
          company,
          role,
        })
        .returning();
      if (!created) throw badRequest("Could not create user");
      const tokens = await issueTokens(created, req);
      res.status(201).json({ user: publicUser(created), tokens });
    } catch (e) {
      next(e);
    }
  },
);

authRouter.post(
  "/login",
  authRateLimit,
  validateBody(loginSchema),
  async (req, res, next) => {
    try {
      const { email, password } = req.body as z.infer<typeof loginSchema>;
      const db = getDb();
      const [user] = await db
        .select()
        .from(users)
        .where(eq(users.email, email))
        .limit(1);
      if (!user || !user.isActive) throw unauthorized("Invalid credentials");
      const ok = await bcrypt.compare(password, user.passwordHash);
      if (!ok) throw unauthorized("Invalid credentials");
      const tokens = await issueTokens(user, req);
      res.json({ user: publicUser(user), tokens });
    } catch (e) {
      next(e);
    }
  },
);

const refreshSchema = z.object({ refresh_token: z.string().min(10) });

authRouter.post(
  "/refresh",
  validateBody(refreshSchema),
  async (req, res, next) => {
    try {
      const { refresh_token } = req.body as z.infer<typeof refreshSchema>;
      const db = getDb();
      const [session] = await db
        .select()
        .from(sessions)
        .where(
          and(
            eq(sessions.refreshToken, refresh_token),
            eq(sessions.isRevoked, false),
          ),
        )
        .limit(1);
      if (!session) throw unauthorized("Refresh token not recognized");
      if (session.expiresAt.getTime() < Date.now()) {
        throw unauthorized("Refresh token expired");
      }
      try {
        const payload = verifyToken(refresh_token);
        if (payload.type !== "refresh") throw unauthorized("Wrong token type");
      } catch {
        throw unauthorized("Invalid refresh token");
      }
      const [user] = await db
        .select()
        .from(users)
        .where(eq(users.id, session.userId))
        .limit(1);
      if (!user || !user.isActive) throw unauthorized("User not active");
      await db
        .update(sessions)
        .set({ isRevoked: true })
        .where(eq(sessions.id, session.id));
      const tokens = await issueTokens(user, req);
      res.json({ user: publicUser(user), tokens });
    } catch (e) {
      next(e);
    }
  },
);

const logoutSchema = z.object({ refresh_token: z.string().optional() });

authRouter.post(
  "/logout",
  validateBody(logoutSchema),
  async (req, res, next) => {
    try {
      const { refresh_token } = req.body as z.infer<typeof logoutSchema>;
      if (refresh_token) {
        const db = getDb();
        await db
          .update(sessions)
          .set({ isRevoked: true })
          .where(eq(sessions.refreshToken, refresh_token));
      }
      res.json({ ok: true });
    } catch (e) {
      next(e);
    }
  },
);

authRouter.get("/me", requireAuth, async (req, res, next) => {
  try {
    const db = getDb();
    const [user] = await db
      .select()
      .from(users)
      .where(eq(users.id, req.user!.sub))
      .limit(1);
    if (!user) throw unauthorized("User not found");
    res.json({ user: publicUser(user) });
  } catch (e) {
    next(e);
  }
});
