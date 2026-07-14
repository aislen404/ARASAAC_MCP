import { notFound } from "next/navigation";

import { getWorkspace } from "../../../../features/workspaces/api";
import { MaterialsInbox } from "../../../../features/workspaces/materials-inbox";
import { WorkspaceProvider } from "../../../../features/workspaces/workspace-context";
import { WorkspaceShell } from "../../../../features/workspaces/workspace-shell";

export default async function WorkspaceInboxPage({
  params,
}: Readonly<{ params: Promise<{ slug: string }> }>) {
  const { slug } = await params;
  const response = await getWorkspace(slug).catch(() => null);
  if (!response) {
    notFound();
  }

  return (
    <WorkspaceProvider workspace={response.workspace} workspaceUrl={`/w/${slug}/mis-materiales`}>
      <WorkspaceShell>
        <MaterialsInbox />
      </WorkspaceShell>
    </WorkspaceProvider>
  );
}