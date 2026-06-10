#!/usr/bin/env node
/**
 * Wave 3 content guard for the Next.js source.
 *
 * Complements the Python scripts/verify_dealix_*.py (which scan docs + sales).
 * This scans the frontend wave3 content/components for:
 *   1. affirmative forbidden CLAIMS (EN + AR), and
 *   2. more than one <PrimaryCta> per page-body component.
 *
 * Note on negation: safe trust copy legitimately references forbidden actions in
 * the negative ("no cold WhatsApp", "we never auto-send", "no scraping"). Those
 * are exactly the messages we want. So dual-use phrases are only flagged when the
 * SAME LINE has no negation marker.
 *
 * Exit 0 on pass, 1 on fail. No dependencies.
 */
import { readdirSync, readFileSync, statSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join, resolve } from "node:path";

const HERE = dirname(fileURLToPath(import.meta.url));
const FRONTEND = resolve(HERE, "..");

const SCAN_DIRS = ["src/content/wave3", "src/components/wave3", "src/lib/wave3"];
const EXT = new Set([".ts", ".tsx"]);

// Affirmative guarantee/fake claims — never acceptable, even negated.
const ALWAYS_FORBIDDEN = [
  "نضمن",
  "ربح مؤكد",
  "guaranteed sales",
  "guaranteed results",
  "guaranteed roi",
  "guarantee roi",
  "guaranteed revenue",
  "guarantee revenue",
  "fake proof",
  "fake testimonial",
];

// Dual-use phrases — fine in the negative ("no cold whatsapp"), bad as a claim.
const DUAL_USE = [
  "cold whatsapp",
  "auto-send",
  "auto send",
  "scraping",
  "purchased list",
  "blast",
  "linkedin automation",
  "مضمون",
  "ضمان مبيعات",
];

const NEGATION = [
  "no ",
  "not ",
  "never",
  "without",
  "don't",
  "doesn't",
  "no-",
  "لا ",
  "بدون",
  "دون ",
  "ليس",
  "ممنوع",
  "يمنع",
  "نحن لا",
  "لا نرسل",
  "blocks",
  "block ",
  "line-through", // struck-through "Dealix is NOT" chips
];

function walk(dir) {
  const out = [];
  let entries;
  try {
    entries = readdirSync(dir);
  } catch {
    return out;
  }
  for (const e of entries) {
    const p = join(dir, e);
    if (statSync(p).isDirectory()) out.push(...walk(p));
    else if (EXT.has(p.slice(p.lastIndexOf(".")))) out.push(p);
  }
  return out;
}

const hasNegation = (line) => NEGATION.some((n) => line.includes(n));

const failures = [];
let scanned = 0;

for (const rel of SCAN_DIRS) {
  for (const file of walk(join(FRONTEND, rel))) {
    scanned++;
    const text = readFileSync(file, "utf8");
    const short = file.replace(FRONTEND + "/", "");

    text.split("\n").forEach((rawLine, i) => {
      const line = rawLine.toLowerCase();
      for (const phrase of ALWAYS_FORBIDDEN) {
        if (line.includes(phrase.toLowerCase())) {
          failures.push(`forbidden claim "${phrase}" in ${short}:${i + 1}`);
        }
      }
      if (!hasNegation(line)) {
        for (const phrase of DUAL_USE) {
          if (line.includes(phrase.toLowerCase())) {
            failures.push(`un-negated "${phrase}" in ${short}:${i + 1}`);
          }
        }
      }
    });

    if (/(Page|Form|Landing|Index)\.tsx$/.test(file)) {
      const count = (text.match(/<PrimaryCta\b/g) || []).length;
      if (count > 1) failures.push(`${short} has ${count} <PrimaryCta> (must be <= 1)`);
    }
  }
}

console.log(`WAVE3_CONTENT_FILES_SCANNED=${scanned}`);
if (failures.length) {
  console.error("WAVE3_CONTENT_PASS=false");
  for (const f of failures) console.error("  - " + f);
  process.exit(1);
}
console.log("WAVE3_CONTENT_PASS=true");
