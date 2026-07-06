export function CsContextHelp() {
  return (
    <section className="cs-help-panel" data-cs="context-help">
      <p className="cs-eyebrow">Ayuda contextual</p>
      <img
        alt="Persona ofreciendo ayuda contextual"
        className="cs-helper-illustration cs-theme-illustration-light"
        height={180}
        src="/convergencia-serena/illustrations/helper-light.svg"
        width={280}
      />
      <img
        alt=""
        aria-hidden="true"
        className="cs-helper-illustration cs-theme-illustration-dark"
        height={180}
        src="/convergencia-serena/illustrations/helper-dark.svg"
        width={280}
      />
      <h2>¿En qué paso estás?</h2>
      <p className="cs-lead">
        Sigue este camino guiado para lograr tus objetivos con claridad y confianza.
      </p>
      <a href="#cs-workflow">Más sobre el flujo →</a>
      <div className="cs-tip" id="cs-accessibility">
        <strong>Consejo de accesibilidad</strong>
        <p>
          Usa descripciones claras en tus colecciones y verifica el contraste de color en tus
          materiales.
        </p>
        <a href="#cs-accessibility">Ver guía rápida →</a>
      </div>
    </section>
  );
}
