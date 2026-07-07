"use client";

import { useMaterialFlow } from "../features/material-builder/flow-context";
import { phaseStatus, workflowSteps } from "./convergencia-serena/workflow-steps";

export function GuidedFlow() {
  const { phase } = useMaterialFlow();
  const activeTitle = workflowSteps[phase][0];

  return (
    <section aria-labelledby="guided-flow-heading" className="guidedFlow">
      <div className="sectionHeading">
        <div>
          <p className="eyebrow">Recorrido gobernado</p>
          <h2 id="guided-flow-heading">Cinco fases, una decisión humana</h2>
        </div>
        <p className="progressLabel">
          <strong>Fase activa:</strong> {activeTitle.toLowerCase()}
        </p>
      </div>
      <ol className="flowSteps">
        {workflowSteps.map(([title, description], index) => {
          const status = phaseStatus(index, phase);
          return (
            <li
              aria-current={index === phase ? "step" : undefined}
              className={index === phase ? "flowStep flowStepActive" : "flowStep"}
              key={title}
            >
              <span aria-hidden="true" className="flowNumber">
                {index + 1}
              </span>
              <div>
                <strong>{title}</strong>
                <span>{description}</span>
                <small>{status}</small>
              </div>
            </li>
          );
        })}
      </ol>
    </section>
  );
}
