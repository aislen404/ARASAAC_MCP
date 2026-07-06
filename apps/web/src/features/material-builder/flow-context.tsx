"use client";

import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

export type FlowPhase = 0 | 1 | 2 | 3 | 4;

type FlowContextValue = {
  phase: FlowPhase;
  setPhase: (phase: FlowPhase) => void;
};

const FlowContext = createContext<FlowContextValue | null>(null);

export function MaterialFlowProvider({ children }: Readonly<{ children: ReactNode }>) {
  const [phase, setPhase] = useState<FlowPhase>(0);
  const value = useMemo(() => ({ phase, setPhase }), [phase]);
  return <FlowContext.Provider value={value}>{children}</FlowContext.Provider>;
}

export function useMaterialFlow(): FlowContextValue {
  const context = useContext(FlowContext);
  if (!context) {
    throw new Error("useMaterialFlow debe usarse dentro de MaterialFlowProvider");
  }
  return context;
}

export function computeFlowPhase(input: {
  hasSearchResults: boolean;
  itemCount: number;
  materialStatus: string | null;
}): FlowPhase {
  if (input.materialStatus === "in_review" || input.materialStatus === "approved") {
    return 4;
  }
  if (input.materialStatus === "draft" || input.materialStatus === "rejected") {
    return 3;
  }
  if (input.itemCount > 0) {
    return 2;
  }
  if (input.hasSearchResults) {
    return 1;
  }
  return 0;
}
