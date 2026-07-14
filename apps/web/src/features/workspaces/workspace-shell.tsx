import type { ReactNode } from "react";

import { ConvergenciaSerenaApp } from "../../components/convergencia-serena/ConvergenciaSerenaApp";
import { WorkspaceHeader } from "./workspace-header";

export function WorkspaceShell({ children }: Readonly<{ children: ReactNode }>) {
  return <ConvergenciaSerenaApp builder={<><WorkspaceHeader />{children}</>} />;
}