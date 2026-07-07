import { ConvergenciaSerenaApp } from "../components/convergencia-serena/ConvergenciaSerenaApp";
import { MaterialBuilderProvider } from "../features/material-builder/builder-context";
import { MaterialFlowProvider } from "../features/material-builder/flow-context";
import { MaterialBuilder } from "./material-builder";

export default function Home() {
  return (
    <MaterialFlowProvider>
      <MaterialBuilderProvider>
        <ConvergenciaSerenaApp builder={<MaterialBuilder embedded />} />
      </MaterialBuilderProvider>
    </MaterialFlowProvider>
  );
}
