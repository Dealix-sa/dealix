import jwt, { type Secret, type SignOptions } from "jsonwebtoken";
import { env } from "../env.js";

export interface JwtPayload {
  sub: string;
  email: string;
  role: string;
  type: "access" | "refresh";
}

export function signAccessToken(
  payload: Omit<JwtPayload, "type">,
): { token: string; expiresAt: number } {
  const secret: Secret = env.JWT_SECRET;
  const options: SignOptions = { expiresIn: env.JWT_ACCESS_TTL_SECONDS };
  const token = jwt.sign({ ...payload, type: "access" }, secret, options);
  return {
    token,
    expiresAt: Date.now() + env.JWT_ACCESS_TTL_SECONDS * 1000,
  };
}

export function signRefreshToken(
  payload: Omit<JwtPayload, "type">,
): { token: string; expiresAt: number } {
  const secret: Secret = env.JWT_SECRET;
  const options: SignOptions = { expiresIn: env.JWT_REFRESH_TTL_SECONDS };
  const token = jwt.sign({ ...payload, type: "refresh" }, secret, options);
  return {
    token,
    expiresAt: Date.now() + env.JWT_REFRESH_TTL_SECONDS * 1000,
  };
}

export function verifyToken(token: string): JwtPayload {
  return jwt.verify(token, env.JWT_SECRET as Secret) as JwtPayload;
}
