import Link from "next/link";

export default function NotFound() {
  return (
    <main className="welcomeMain" id="main-content">
      <section className="welcomeCard workspaceNotFoundCard">
        <p className="eyebrow">No disponible</p>
        <h1>No hemos encontrado este workspace o material.</h1>
        <p className="helpText">
          Este enlace no existe, ya no está disponible o no pertenece al workspace actual.
        </p>
        <Link className="workspaceLinkButton" href="/">
          Volver a inicio
        </Link>
      </section>
    </main>
  );
}