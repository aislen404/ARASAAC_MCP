import { notFound } from "next/navigation";

import { MaterialBuilderProvider } from "../../../../features/material-builder/builder-context";
import { MaterialFlowProvider } from "../../../../features/material-builder/flow-context";
import { MaterialBuilder } from "../../../../features/material-builder/material-builder";
import { getWorkspace } from "../../../../features/workspaces/api";
import { WorkspaceProvider } from "../../../../features/workspaces/workspace-context";
import { WorkspaceShell } from "../../../../features/workspaces/workspace-shell";

export default async function WorkspaceNewPage({
  params,
}: Readonly<{ params: Promise<{ slug: string }> }>) {
  const { slug } = await params;
  const response = await getWorkspace(slug).catch(() => null);
  if (!response) {
    notFound();
  }

  return (
    <WorkspaceProvider workspace={response.workspace} workspaceUrl={`/w/${slug}/mis-materiales`}>
      <MaterialFlowProvider>
        <MaterialBuilderProvider>
          <WorkspaceShell>
            <MaterialBuilder embedded />
          </WorkspaceShell>
        </MaterialBuilderProvider>
      </MaterialFlowProvider>
    </WorkspaceProvider>
  );
}