import { CsIcon, type CsIconName } from "./CsIcon";

const nav: Array<{ label: string; href: string; icon: CsIconName; current?: boolean; soft?: boolean }> = [
  { label: "Inicio", href: "#cs-main", icon: "home", current: true },
  { label: "Explorar", href: "#cs-builder", icon: "search" },
  { label: "Colecciones", href: "#cs-builder", icon: "folder" },
  { label: "Asistente guiado", href: "#cs-workflow", icon: "check", soft: true },
  { label: "Validación", href: "#cs-review", icon: "shield" },
  { label: "Accesibilidad", href: "#cs-accessibility", icon: "accessibility" },
  { label: "Actividad", href: "#cs-bottom", icon: "activity" },
];

export function CsSideRail() {
  return (
    <aside className="cs-side-rail" data-cs="side-rail">
      <p className="cs-eyebrow">Espacio de trabajo</p>
      <nav aria-label="Navegación principal Convergencia Serena">
        <ul className="cs-nav-list">
          {nav.map((item) => (
            <li key={item.label}>
              <a className="cs-nav-link" href={item.href} aria-current={item.current ? "page" : undefined} data-active={item.soft ? "soft" : undefined}>
                <span className="cs-icon-box"><CsIcon name={item.icon} /></span>{item.label}
              </a>
            </li>
          ))}
        </ul>
      </nav>
      <div className="cs-tip">
        <p className="cs-eyebrow">Gobernanza</p>
        <strong>Revisión humana obligatoria</strong>
        <p>La IA propone texto; una persona selecciona cada pictograma real de ARASAAC.</p>
      </div>
    </aside>
  );
}
