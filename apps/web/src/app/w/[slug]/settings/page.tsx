import { notFound } from "next/navigation";

import { getWorkspace } from "../../../../features/workspaces/api";
import { WorkspaceProvider } from "../../../../features/workspaces/workspace-context";
import { WorkspaceSettingsForm } from "../../../../features/workspaces/workspace-settings-form";
import { WorkspaceShell } from "../../../../features/workspaces/workspace-shell";

export default async function WorkspaceSettingsPage({
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
        <section className="workspacePanel">
          <p className="eyebrow">Ajustes</p>
          <h2>Identidad del workspace</h2>
          <p>Slug: {response.workspace.slug}</p>
          <p>Nombre actual: {response.workspace.display_name ?? "Sin nombre visible"}</p>
        </section>
        <WorkspaceSettingsForm
          initialDisplayName={response.workspace.display_name}
          slug={response.workspace.slug}
        />
      </WorkspaceShell>
    </WorkspaceProvider>
  );
}