"use client";

import { useEffect } from "react";

import type { Material } from "./types";
import { MaterialBuilderProvider, useMaterialBuilderContext } from "./builder-context";
import { MaterialBuilder } from "./material-builder";

function HydratedMaterialBuilderInner({ material }: Readonly<{ material: Material }>) {
  const builder = useMaterialBuilderContext();

  useEffect(() => {
    builder.loadMaterial(material);
  }, [builder, material]);

  return (
    <>
      <MaterialBuilder embedded />
      <section className="workspacePanel" id="audit">
        <p className="eyebrow">Detalle</p>
        <h2>{material.status === "approved" ? "Material en modo lectura" : "Material cargado"}</h2>
        <p>{material.title}</p>
        <p>Estado: {material.status}</p>
      </section>
    </>
  );
}

export function HydratedMaterialBuilder({ material }: Readonly<{ material: Material }>) {
  return (
    <MaterialBuilderProvider>
      <HydratedMaterialBuilderInner material={material} />
    </MaterialBuilderProvider>
  );
}