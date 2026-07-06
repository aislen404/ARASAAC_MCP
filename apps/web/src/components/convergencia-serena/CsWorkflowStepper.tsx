"use client";

import { useMaterialFlow } from "../../features/material-builder/flow-context";
import { CsIcon, type CsIconName } from "./CsIcon";
import { phaseStatus, workflowStepIcons, workflowSteps } from "./workflow-steps";

export function CsWorkflowStepper() {
  const { phase } = useMaterialFlow();

  return (
    <ol
      aria-label="Flujo guiado de creación"
      className="cs-stepper"
      data-cs="workflow-stepper"
      id="cs-workflow"
    >
      {workflowSteps.map(([title, text], index) => {
        const state =
          index < phase ? "done" : index === phase ? "active" : "pending";
        const status = phaseStatus(index, phase);
        const icon = workflowStepIcons[index] as CsIconName;

        return (
          <li
            aria-current={index === phase ? "step" : undefined}
            className="cs-step-card"
            data-state={state}
            key={title}
          >
            <span className="cs-step-number">{index + 1}</span>
            <CsIcon name={icon} />
            <strong>{title}</strong>
            <span>{text}</span>
            <small className="cs-metric-label">{status}</small>
          </li>
        );
      })}
    </ol>
  );
}
