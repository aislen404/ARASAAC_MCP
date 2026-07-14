const API_URL = "/backend";

import type { ValidationReport } from "./types";

export async function api<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as
      | { detail?: string }
      | null;
    throw new Error(body?.detail ?? `Error HTTP ${response.status}.`);
  }
  return (await response.json()) as T;
}

export function validateMaterial(path: string): Promise<ValidationReport> {
  return api<ValidationReport>(path, {
    method: "POST",
  });
}

export function buildWorkspacePath(slug: string, path: string): string {
  return slug ? `/api/workspaces/${slug}${path}` : `/api${path}`;
}
