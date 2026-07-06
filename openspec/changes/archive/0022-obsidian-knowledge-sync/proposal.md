# Proposal — 0022-obsidian-knowledge-sync

## Problema

El conocimiento operativo del proyecto vive en el repositorio, mientras que el
equipo consulta Obsidian desde iCloud. Una copia manual se desactualiza, puede
duplicar contenido y no ofrece una forma verificable de saber si ambas superficies
coinciden.

## Propuesta

Incorporar una sincronización unidireccional repositorio → bóveda
`ARASAAC_Project` que:

- copie únicamente documentación, OpenSpecs, reglas y conocimiento canónico;
- mantenga un manifiesto con hashes de los archivos administrados;
- elimine solo archivos obsoletos previamente creados por el sincronizador;
- preserve cualquier nota manual ajena al manifiesto;
- permita sincronizar y comprobar mediante Make;
- se ejecute después de commits y merges mediante hooks Git versionados;
- nunca bloquee una operación Git si iCloud no está disponible.

## Fuera de alcance

- Sincronización Obsidian → repositorio.
- Copia de código fuente, secretos, historial Git, builds o dependencias.
- Instalación global de hooks para otros repositorios.
- Modificación automática de notas manuales no administradas.
