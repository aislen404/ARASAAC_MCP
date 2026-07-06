"use client";

import { createContext, useContext, type ReactNode } from "react";

import { useMaterialBuilder } from "./use-material-builder";

type MaterialBuilderValue = ReturnType<typeof useMaterialBuilder>;

const BuilderContext = createContext<MaterialBuilderValue | null>(null);

export function MaterialBuilderProvider({ children }: Readonly<{ children: ReactNode }>) {
  const builder = useMaterialBuilder();
  return <BuilderContext.Provider value={builder}>{children}</BuilderContext.Provider>;
}

export function useMaterialBuilderContext(): MaterialBuilderValue {
  const context = useContext(BuilderContext);
  if (!context) {
    throw new Error("useMaterialBuilderContext debe usarse dentro de MaterialBuilderProvider");
  }
  return context;
}
