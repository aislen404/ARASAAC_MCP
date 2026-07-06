# Design — 0012-export-engine

La exportación es una función pura que primero valida estado, revisión y licencia.
HTML escapa todo texto. PDF se deriva del mismo contenido mediante una librería
determinista. No descarga ni transforma pictogramas; usa URLs oficiales.
