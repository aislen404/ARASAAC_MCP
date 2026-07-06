import type { ReactNode } from "react";

import { GuidedFlow } from "./guided-flow";
import { ThemeToggle } from "./theme-toggle";

const navigation = [
  ["Inicio", "#inicio"],
  ["Crear material", "#workspace"],
  ["Explorar ARASAAC", "#create-heading"],
  ["Vista previa", "#preview-heading"],
  ["Revisión", "#review-heading"],
] as const;

export function AppShell({ children }: Readonly<{ children: ReactNode }>) {
  return (
    <>
      <a className="skipLink" href="#main-content">
        Saltar al contenido principal
      </a>
      <header className="productHeader" id="inicio">
        <a className="brand" href="#inicio">
          <span aria-hidden="true" className="brandMark">
            AS
          </span>
          <span>
            <strong>ARASAAC Social</strong>
            <small>Materiales accesibles · no comercial</small>
          </span>
        </a>
        <div className="headerActions">
          <p className="humanReviewStatus">
            <span aria-hidden="true">✓</span>
            Revisión humana obligatoria
          </p>
          <ThemeToggle />
        </div>
      </header>
      <div className="appFrame">
        <aside className="sideRail">
          <nav aria-label="Navegación principal">
            <p className="navLabel">Espacio de trabajo</p>
            <ul>
              {navigation.map(([label, href], index) => (
                <li key={label}>
                  <a aria-current={index === 0 ? "page" : undefined} href={href}>
                    <span aria-hidden="true">{index + 1}</span>
                    {label}
                  </a>
                </li>
              ))}
            </ul>
          </nav>
          <aside aria-labelledby="help-heading" className="contextHelp">
            <p className="eyebrow">Ayuda contextual</p>
            <h2 id="help-heading">Antes de empezar</h2>
            <p>
              Trabaja con situaciones genéricas. No incluyas nombres, contacto,
              diagnósticos ni información sensible.
            </p>
            <a href="#workspace">Ir al constructor</a>
          </aside>
        </aside>
        <main id="main-content">
          <section aria-labelledby="welcome-heading" className="welcome">
            <div>
              <p className="eyebrow">Convergencia Serena</p>
              <h1 id="welcome-heading">Crear con claridad. Revisar con criterio.</h1>
              <p className="welcomeLead">
                Un espacio guiado para preparar materiales accesibles con
                pictogramas reales de ARASAAC y control humano en cada decisión.
              </p>
            </div>
            <dl className="metricGrid" aria-label="Garantías del flujo">
              <div>
                <dt>5</dt>
                <dd>fases guiadas</dd>
              </div>
              <div>
                <dt>100%</dt>
                <dd>selección humana</dd>
              </div>
              <div>
                <dt>0</dt>
                <dd>exportaciones sin aprobar</dd>
              </div>
            </dl>
          </section>
          <GuidedFlow />
          <section aria-labelledby="builder-heading" className="builderIntro">
            <p className="eyebrow">Área de trabajo</p>
            <h2 id="builder-heading">Continúa con tu material</h2>
            <p>
              La IA, si está habilitada, solo propone texto. Tú eliges cada
              pictograma y una persona revisa el resultado final.
            </p>
          </section>
          {children}
          <section aria-labelledby="accessibility-heading" className="commitments">
            <div>
              <p className="eyebrow">Accesibilidad integrada</p>
              <h2 id="accessibility-heading">Criterios visibles y verificables</h2>
            </div>
            <ul aria-label="Compromisos de accesibilidad">
              <li>WCAG 2.2 AA</li>
              <li>WAI-ARIA</li>
              <li>Teclado</li>
              <li>Foco visible</li>
              <li>Contraste</li>
              <li>Targets de 44 px</li>
            </ul>
          </section>
        </main>
      </div>
      <footer className="siteFooter">
        <p>
          Los símbolos pictográficos utilizados son propiedad del Gobierno de
          Aragón y han sido creados por Sergio Palao para ARASAAC, que los
          distribuye bajo licencia Creative Commons BY-NC-SA.
        </p>
        <p>
          Plataforma social no comercial · Sin diagnóstico · Sin datos personales
        </p>
      </footer>
    </>
  );
}
