"use client";

import { useMaterialFlow } from "../../features/material-builder/flow-context";
import { CsIllustration } from "./CsIllustration";
import { buildWorkspaceSuggestions } from "./workspace-suggestions";

export function CsSuggestionStrip() {
  const { phase } = useMaterialFlow();
  const suggestions = buildWorkspaceSuggestions(phase);

  return (
    <section
      aria-label="Sugerencias para ti"
      className="cs-panel cs-main-inner"
      id="cs-suggestions"
    >
      <div className="cs-chip-row" style={{ justifyContent: "space-between" }}>
        <h3 style={{ margin: 0 }}>Sugerencias para ti</h3>
        <a href="#cs-suggestions">Ver todas →</a>
      </div>
      <div className="cs-suggestion-grid">
        {suggestions.map((suggestion) => (
          <a className="cs-suggestion-card" href={suggestion.href} key={suggestion.title}>
            <CsIllustration
              alt=""
              ariaHidden
              className="cs-suggestion-illustration"
              height={72}
              src={`/convergencia-serena/illustrations/${suggestion.illustration}`}
              width={96}
            />
            <strong>{suggestion.title}</strong>
            <p className="cs-metric-label">{suggestion.description}</p>
          </a>
        ))}
      </div>
    </section>
  );
}
