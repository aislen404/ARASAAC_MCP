import type { ReactNode } from "react";

import { CsBottomStrip } from "./CsBottomStrip";
import { CsContextHelp } from "./CsContextHelp";
import { CsGuidedWorkspace } from "./CsGuidedWorkspace";
import { CsHeader } from "./CsHeader";
import { CsSideRail } from "./CsSideRail";

export function ConvergenciaSerenaApp({ builder }: Readonly<{ builder: ReactNode }>) {
  return (
    <div className="cs-root" data-cs="app">
      <a className="skipLink" href="#cs-main">
        Saltar al contenido principal
      </a>
      <CsHeader />
      <div className="cs-shell">
        <div className="cs-grid">
          <CsSideRail />
          <main className="cs-main-stack" id="cs-main">
            <CsGuidedWorkspace builder={builder} />
          </main>
          <aside aria-label="Ayuda contextual" className="cs-right-stack">
            <CsContextHelp />
          </aside>
        </div>
        <CsBottomStrip />
      </div>
      <footer className="cs-footer">
        <p>
          Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón y han sido
          creados por Sergio Palao para ARASAAC, que los distribuye bajo licencia Creative
          Commons BY-NC-SA.
        </p>
        <p>Plataforma social no comercial · Sin diagnóstico · Sin datos personales</p>
      </footer>
    </div>
  );
}
