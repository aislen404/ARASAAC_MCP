"use client";

type ErrorProps = {
  error: Error & { digest?: string };
  reset: () => void;
};

export default function ErrorPage({ error, reset }: Readonly<ErrorProps>) {
  return (
    <main className="errorState" id="main-content">
      <h1>No se pudo cargar la página</h1>
      <p role="alert">{error.message || "Ha ocurrido un error inesperado."}</p>
      <button onClick={reset} type="button">
        Reintentar
      </button>
    </main>
  );
}
