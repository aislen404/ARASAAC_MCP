import { notFound } from "next/navigation";

import { HydratedMaterialBuilder } from "../../../../../features/material-builder/hydrated-material-builder";
import { MaterialFlowProvider } from "../../../../../features/material-builder/flow-context";
import {
  getWorkspace,
  getWorkspaceMaterial,
} from "../../../../../features/workspaces/api";
import { WorkspaceProvider } from "../../../../../features/workspaces/workspace-context";
import { WorkspaceShell } from "../../../../../features/workspaces/workspace-shell";

export default async function WorkspaceMaterialPage({
  params,
}: Readonly<{ params: Promise<{ slug: string; materialId: string }> }>) {
  const { slug, materialId } = await params;
  const [workspace, material] = await Promise.all([
    getWorkspace(slug).catch(() => null),
    getWorkspaceMaterial(slug, materialId).catch(() => null),
  ]);
  if (!workspace || !material) {
    notFound();
  }

  return (
    <WorkspaceProvider workspace={workspace.workspace} workspaceUrl={`/w/${slug}/mis-materiales`}>
      <MaterialFlowProvider>
        <WorkspaceShell>
          <HydratedMaterialBuilder material={material.material} />
        </WorkspaceShell>
      </MaterialFlowProvider>
    </WorkspaceProvider>
  );
}