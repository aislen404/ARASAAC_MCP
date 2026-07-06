"use client";

import { useMaterialBuilderContext } from "./builder-context";
import { CreationForm } from "./creation-form";
import { EditorPanel } from "./editor-panel";
import { ReviewPanel } from "./review-panel";

export function MaterialBuilder({ embedded = false }: Readonly<{ embedded?: boolean }>) {
  const builder = useMaterialBuilderContext();

  return (
    <div
      aria-busy={builder.busy}
      aria-label="Constructor de materiales"
      className={embedded ? "cs-builder-embedded" : "workspace"}
      id="workspace"
    >
      <CreationForm builder={builder} embedded={embedded} />
      <EditorPanel builder={builder} embedded={embedded} />
      <ReviewPanel builder={builder} embedded={embedded} />
    </div>
  );
}
