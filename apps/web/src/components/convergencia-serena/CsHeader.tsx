import { CsIcon } from "./CsIcon";
import { CsThemeToggle } from "./CsThemeToggle";

export function CsHeader() {
  return (
    <header className="cs-header" data-cs="header">
      <a aria-label="ARASAAC Social MCP Platform" className="cs-brand" href="#cs-main">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          alt=""
          className="cs-brand-mark"
          height={48}
          src="/convergencia-serena/brand/monogram.svg"
          width={48}
        />
        <span>
          <strong>ARASAAC</strong>
          <small>Social MCP Platform · Encontrar · Organizar · Compartir impacto</small>
        </span>
      </a>
      <div className="cs-header-actions">
        <div aria-label="Garantías de interfaz" className="cs-badge-row" role="list">
          <span className="cs-badge" role="listitem">
            <CsIcon name="contrast" />{" "}
            <span>
              WCAG 2.2 AA<small>Conforme</small>
            </span>
          </span>
          <span className="cs-badge" role="listitem">
            <CsIcon name="keyboard" />{" "}
            <span>
              Teclado<small>Navegable</small>
            </span>
          </span>
          <span className="cs-badge" role="listitem">
            <CsIcon name="leaf" />{" "}
            <span>
              Contraste alto<small>Legible</small>
            </span>
          </span>
        </div>
        <div className="cs-header-controls">
          <CsThemeToggle />
        </div>
      </div>
    </header>
  );
}
