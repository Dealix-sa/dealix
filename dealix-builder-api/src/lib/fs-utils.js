import fs from "node:fs/promises";
import path from "node:path";
import { ACTIVE_ROOT } from "./paths.js";

export async function exists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

export async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

export async function readText(p) {
  return fs.readFile(p, "utf8");
}

export async function writeText(p, text) {
  await ensureDir(path.dirname(p));
  await fs.writeFile(p, text, "utf8");
}

export async function appendText(p, text) {
  await ensureDir(path.dirname(p));
  await fs.appendFile(p, text, "utf8");
}

export async function listFiles(root = ACTIVE_ROOT, max = 500) {
  const out = [];

  async function walk(dir) {
    if (out.length >= max) return;
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const e of entries) {
      if (out.length >= max) return;
      if (["node_modules", ".git", ".venv", "dist", "build", ".next"].includes(e.name)) continue;
      const full = path.join(dir, e.name);
      if (e.isDirectory()) await walk(full);
      else out.push(path.relative(ACTIVE_ROOT, full));
    }
  }

  await walk(root);
  return out;
}
