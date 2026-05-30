import { writeText } from "../lib/fs-utils.js";
import path from "node:path";
import { API_ROOT } from "../lib/paths.js";

export async function saveReport(name, content) {
  const stamp = new Date().toISOString().replace(/[:.]/g, "-");
  const file = path.join(API_ROOT, "src", "reports", `${stamp}-${name}.md`);
  await writeText(file, content);
  return file;
}
