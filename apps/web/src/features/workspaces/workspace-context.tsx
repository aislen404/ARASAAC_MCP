"use client";

import { createContext, useContext, type ReactNode } from "react";

import type { Workspace } from "./types";

type WorkspaceContextValue = {
  workspace: Workspace;
  workspaceUrl: string;
};

const WorkspaceContext = createContext<WorkspaceContextValue | null>(null);

export function WorkspaceProvider({
  workspace,
  workspaceUrl,
  children,
}: Readonly<{ workspace: Workspace; workspaceUrl: string; children: ReactNode }>) {
  return (
    <WorkspaceContext.Provider value={{ workspace, workspaceUrl }}>
      {children}
    </WorkspaceContext.Provider>
  );
}

export function useWorkspace(): WorkspaceContextValue {
  const context = useContext(WorkspaceContext);
  if (!context) {
    throw new Error("useWorkspace debe usarse dentro de WorkspaceProvider");
  }
  return context;
}