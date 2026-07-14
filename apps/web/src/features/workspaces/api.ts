import type { MaterialListResponse, MaterialResponse, WorkspaceResponse } from "./types";

const API_URL = "/backend";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...options?.headers },
  });
  if (!response.ok) {
    const body = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(body?.detail ?? `Error HTTP ${response.status}.`);
  }
  return (await response.json()) as T;
}

export function createWorkspace(display_name?: string): Promise<WorkspaceResponse> {
  return request<WorkspaceResponse>("/api/workspaces", {
    method: "POST",
    body: JSON.stringify(display_name ? { display_name } : {}),
  });
}

export function getWorkspace(slug: string): Promise<WorkspaceResponse> {
  return request<WorkspaceResponse>(`/api/workspaces/${slug}`);
}

export function updateWorkspace(
  slug: string,
  display_name: string | null,
): Promise<WorkspaceResponse> {
  return request<WorkspaceResponse>(`/api/workspaces/${slug}`, {
    method: "PATCH",
    body: JSON.stringify({ display_name }),
  });
}

export function listWorkspaceMaterials(
  slug: string,
  params: { status?: string; q?: string; limit?: number; offset?: number } = {},
): Promise<MaterialListResponse> {
  const search = new URLSearchParams();
  if (params.status) search.set("status", params.status);
  if (params.q) search.set("q", params.q);
  if (params.limit) search.set("limit", String(params.limit));
  if (params.offset) search.set("offset", String(params.offset));
  const query = search.toString();
  return request<MaterialListResponse>(`/api/workspaces/${slug}/materials${query ? `?${query}` : ""}`);
}

export function getWorkspaceMaterial(
  slug: string,
  materialId: string,
): Promise<MaterialResponse> {
  return request<MaterialResponse>(`/api/workspaces/${slug}/materials/${materialId}`);
}