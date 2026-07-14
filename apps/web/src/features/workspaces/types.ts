export type Workspace = {
  workspace_id: string;
  slug: string;
  display_name: string | null;
  created_at: string;
  updated_at: string;
};

export type WorkspaceSummary = {
  workspace_id: string;
  slug: string;
  display_name: string | null;
};

export type WorkspaceResponse = {
  workspace: Workspace;
};

export type WorkspaceMaterialStatus = "draft" | "in_review" | "approved" | "rejected";

export type WorkspaceMaterial = {
  material_id: string;
  title: string;
  material_type:
    | "visual_agenda"
    | "communication_board"
    | "accessible_document"
    | "social_story"
    | "signage";
  status: WorkspaceMaterialStatus;
  attribution_text: string;
  updated_at: string;
  created_at: string;
  version: number;
};

export type MaterialResponse = {
  material: WorkspaceMaterial;
  workspace?: WorkspaceSummary;
};

export type MaterialListResponse = {
  materials: WorkspaceMaterial[];
  total: number;
  limit: number;
  offset: number;
  workspace: WorkspaceSummary;
};