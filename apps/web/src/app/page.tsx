import { MaterialBuilder } from "./material-builder";

export default function Home() {
  return (
    <>
      <a className="skipLink" href="#main-content">
        Saltar al contenido principal
      </a>
      <header className="siteHeader">
        <div>
          <p className="eyebrow">MVP social · no comercial</p>
          <h1>ARASAAC Social MCP Platform</h1>
        </div>
        <p className="status">
          <span aria-hidden="true" className="statusDot" />
          Revisión humana obligatoria
        </p>
      </header>
      <main id="main-content">
        <MaterialBuilder />
      </main>
      <footer className="siteFooter">
        Los símbolos pictográficos utilizados son propiedad del Gobierno de Aragón
        y han sido creados por Sergio Palao para ARASAAC, que los distribuye bajo
        licencia Creative Commons BY-NC-SA.
      </footer>
    </>
  );
}
