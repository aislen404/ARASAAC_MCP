const limits = [
  "Sin integración ni consultas a ARASAAC",
  "Sin generación o exportación de materiales",
  "Sin autenticación ni datos personales",
  "Servidor MCP deshabilitado y sin tools",
];

export default function Home() {
  return (
    <main>
      <section aria-labelledby="project-title" className="card">
        <p className="eyebrow">MVP-0 · Project foundation</p>
        <h1 id="project-title">ARASAAC Social MCP Platform</h1>
        <p className="status">
          <span aria-hidden="true" className="statusDot" />
          Base técnica disponible
        </p>
        <p>
          Esta entrega establece únicamente la estructura de servicios y sus
          comprobaciones de estado.
        </p>
        <h2>Límites actuales</h2>
        <ul>
          {limits.map((limit) => (
            <li key={limit}>{limit}</li>
          ))}
        </ul>
      </section>
    </main>
  );
}
