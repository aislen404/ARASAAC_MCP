# Design — 0016-review-workflow

La API expone submit y decide. No existe aprobación implícita. Cada transición
crea versión/evento; editar un aprobado genera un nuevo draft.
