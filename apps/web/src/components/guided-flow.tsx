const steps = [
  ["Definir necesidad", "Describe un escenario genérico y sin datos personales."],
  ["Explorar pictogramas", "Consulta exclusivamente candidatos reales de ARASAAC."],
  ["Organizar material", "Selecciona, ordena y ajusta cada elemento."],
  ["Validar accesibilidad", "Comprueba claridad, secuencia y atribución."],
  ["Revisar y compartir", "Una persona debe aprobar antes de exportar."],
] as const;

export function GuidedFlow() {
  return (
    <section aria-labelledby="guided-flow-heading" className="guidedFlow">
      <div className="sectionHeading">
        <div>
          <p className="eyebrow">Recorrido gobernado</p>
          <h2 id="guided-flow-heading">Cinco fases, una decisión humana</h2>
        </div>
        <p className="progressLabel">
          <strong>Fase activa:</strong> definir necesidad
        </p>
      </div>
      <ol className="flowSteps">
        {steps.map(([title, description], index) => (
          <li
            aria-current={index === 0 ? "step" : undefined}
            className={index === 0 ? "flowStep flowStepActive" : "flowStep"}
            key={title}
          >
            <span aria-hidden="true" className="flowNumber">
              {index + 1}
            </span>
            <div>
              <strong>{title}</strong>
              <span>{description}</span>
              <small>{index === 0 ? "En curso" : "Pendiente"}</small>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}
