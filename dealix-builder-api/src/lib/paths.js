import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
export const API_ROOT = path.resolve(here, "../..");
export const REPO_ROOT = path.resolve(API_ROOT, process.env.DEALIX_ROOT || "..");
export const ACTIVE_SCOPE = process.env.DEALIX_ACTIVE_SCOPE || "dealix-v2";
export const ACTIVE_ROOT = path.resolve(REPO_ROOT, ACTIVE_SCOPE);

export function safeJoinInsideActive(...parts) {
  const target = path.resolve(ACTIVE_ROOT, ...parts);
  if (!target.startsWith(ACTIVE_ROOT)) {
    throw new Error("Path escapes active Dealix scope");
  }
  return target;
}
