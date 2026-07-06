import { CsIcon } from "./CsIcon";

const principles = [
  ["leaf", "Camino guiado", "Paso a paso claro y amable que reduce la carga cognitiva."],
  ["analytics", "Calma operativa", "Información organizada, jerarquizada y accionable."],
  ["eye", "Foco visible", "Estados de foco siempre visibles para teclado."],
  ["people", "Centrado en personas", "Lenguaje humano y experiencias que respetan ritmos."],
  ["shield", "Accesible por diseño", "WCAG 2.2 AA, WAI-ARIA y targets generosos."],
] as const;

export function CsBottomStrip() {
  return (
    <section className="cs-bottom-strip" data-cs="bottom-strip" id="cs-bottom" aria-label="Principios de diseño Convergencia Serena">
      <article>
        <p className="cs-eyebrow">Paleta de color</p>
        <div className="cs-chip-row">
          {['#0B1D34','#334155','#6C8F7A','#C86F4A','#F7F3EE','#0EA5E9'].map((c) => <span key={c} className="cs-chip"><span aria-hidden="true" style={{ background:c, width:18, height:18, borderRadius:6, display:'inline-block', border:'1px solid var(--cs-border)' }} />{c}</span>)}
        </div>
      </article>
      {principles.map(([icon, title, text]) => (
        <article key={title}>
          <CsIcon name={icon} />
          <strong>{title}</strong>
          <p className="cs-metric-label">{text}</p>
        </article>
      ))}
    </section>
  );
}
