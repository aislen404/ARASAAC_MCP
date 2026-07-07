export type Pictogram = {
  pictogram_id: number;
  label: string;
  source_url: string;
  origin: "ARASAAC";
  author: "Sergio Palao";
  owner: "Gobierno de Aragón";
  license: "CC BY-NC-SA";
  retrieved_at: string;
};

export type SelectedItem = {
  key: string;
  text: string;
  pictogram: Pictogram;
};

export type MaterialStatus = "draft" | "in_review" | "approved" | "rejected";

export type Material = {
  material_id: string;
  title: string;
  material_type:
    | "visual_agenda"
    | "communication_board"
    | "accessible_document"
    | "social_story"
    | "signage";
  status: MaterialStatus;
  attribution_text: string;
};

export type SearchResponse = {
  candidates: Pictogram[];
  requires_human_selection: true;
};

export type AIStatus = {
  available: boolean;
  provider: string;
  model: string | null;
  reason: string | null;
  generates_pictograms: false;
  requires_human_selection: true;
  stores_input: false;
};

export type AIResolvedItem = {
  text: string;
  search_term: string;
  candidates: Pictogram[];
};

export type AIPlanResponse = {
  summary: string;
  items: AIResolvedItem[];
  provider: string;
  model: string;
  requires_human_selection: true;
  creates_material: false;
  stores_input: false;
  warning: string;
};

export type MaterialResponse = {
  material: Material;
};

export type ExportResponse = {
  filename: string;
  media_type: string;
  content_base64: string;
};

export type MaterialBuilderType = "agenda" | "board" | "document" | "story" | "signage";
