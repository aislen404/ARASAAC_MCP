import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const source = path.join(root, "assets");
const target = path.join(root, "public", "convergencia-serena");
const folders = ["brand", "icons", "illustrations", "patterns"];

if (!existsSync(source)) {
  console.error(`Missing asset source: ${source}`);
  process.exit(1);
}

if (existsSync(target)) {
  rmSync(target, { recursive: true, force: true });
}
mkdirSync(target, { recursive: true });

for (const folder of folders) {
  const from = path.join(source, folder);
  if (!existsSync(from)) {
    console.error(`Missing asset folder: ${from}`);
    process.exit(1);
  }
  cpSync(from, path.join(target, folder), { recursive: true });
}

console.log(`Synced Convergencia Serena assets to ${target}`);
