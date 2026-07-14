---
name: export-with-manifest
description: Generar HTML/PDF/DOCX/PPTX/ZIP con atribución visible y manifest ARASAAC completo.
inputs:
  - material_id
  - format          # html | pdf | docx | pptx | zip | images
  - locale
outputs:
  - Archivo exportado
  - Manifest JSON incrustado + visible en documento
invoked_by_agents: [build]
gates: [license]
---

# Skill: export-with-manifest

## Cuándo usarla
- Un material en estado `approved` va a exportarse.
- Se regenera un export tras cambio de plantilla.

## Procedimiento paso a paso

1. **Verificar precondition**: material en estado `approved`. Si no, **rechazar** y avisar de invocar `human-review-gate` primero.
2. **Cargar plantilla** por formato:
   - HTML → `packages/export/templates/<type>.html.j2`
   - PDF → mismo HTML + WeasyPrint/Playwright print.
   - DOCX → `python-docx` con plantilla `.docx`.
   - PPTX → `python-pptx`.
   - ZIP → paquete con HTML + assets + manifest.
   - Images → SVG/PNG estáticos por página.
3. **Recopilar manifest de atribución** (uno por pictograma usado):
   ```json
   {
     "material_id": "abc-123",
     "generated_at": "2025-01-20T15:00:00Z",
     "pictograms": [
       {
         "id": 2547,
         "url": "https://api.arasaac.org/api/pictograms/2547",
         "author": "Sergio Palao",
         "owner": "Gobierno de Aragón",
         "license": "CC BY-NC-SA",
         "retrieved_at": "2025-01-15T10:00:00Z"
       }
     ]
   }
   ```
4. **Inyectar atribución VISIBLE** en el documento:
   - Pie de página / última slide / sección "Créditos".
   - Texto mínimo obligatorio:
     > Pictogramas: autor Sergio Palao. Origen: ARASAAC (http://www.arasaac.org).
     > Licencia: CC BY-NC-SA. Propiedad: Gobierno de Aragón.
5. **Incrustar manifest JSON** en el archivo:
   - HTML/ZIP → archivo `manifest.json` adjunto.
   - PDF/DOCX/PPTX → como metadata XMP/custom-property.
6. **Registrar evento** de export con audit log (material_id, format, user, timestamp).
7. **Devolver** URL descarga + hash del archivo.

## Gate `license` — checklist obligatorio

- [ ] Atribución visible en el archivo (no solo en metadata).
- [ ] Manifest JSON completo (todos los pictogramas usados).
- [ ] URL de origen a arasaac.org preservada.
- [ ] Sin modificación del pictograma (SVG/PNG originales).
- [ ] Sin claim de autoría distinta a Palao/Gobierno de Aragón.

## Ejemplo mínimo (HTML footer)

```html
<footer class="arasaac-credits">
  Pictogramas: <strong>Sergio Palao</strong>.
  Origen: <a href="http://www.arasaac.org">ARASAAC</a>.
  Licencia: <strong>CC BY-NC-SA</strong>.
  Propiedad: <strong>Gobierno de Aragón</strong>.
</footer>
```

## Errores comunes

- ❌ Atribución solo en metadata (invisible al usuario) → viola gate `license`.
- ❌ Exportar sin `approved` → viola regla absoluta #5.
- ❌ Reescalar / recolorear pictogramas → viola regla absoluta #3.
- ❌ Faltar un pictograma en el manifest → auditoría inconsistente.

## Ver también

- Skill: [`arasaac-fetch`](../arasaac-fetch/SKILL.md)
- Persona: `.agents/personas/export-document.persona.md`
- Regla: `.agents/rules/export-license.md`
- Doc: `NOTICE-ARASAAC.md`
