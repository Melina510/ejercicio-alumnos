# Entrega CI/CD - Simulador Mundial 2026

## Resumen

Implemente el pipeline CI/CD del Simulador Mundial 2026 con GitHub Actions.
La entrega demuestra el flujo completo pedido en la consigna: workflow con 5 jobs,
pipeline rojo diagnosticado, fix aplicado y pipeline verde con deploy a GitHub Pages.

## Links de entrega

- Repositorio: https://github.com/Melina510/ejercicio-alumnos
- Run exitoso de GitHub Actions: https://github.com/Melina510/ejercicio-alumnos/actions/runs/28205843911
- Sitio publicado en GitHub Pages: https://melina510.github.io/ejercicio-alumnos/

## Workflow implementado

El workflow `.github/workflows/ci.yml` ejecuta 5 jobs encadenados:

1. `1 Lint`: valida el codigo con Ruff.
2. `2 Tests + Coverage`: ejecuta los tests con cobertura y genera `coverage.xml`.
3. `3 Quality Gate`: valida cobertura minima de 80% parseando `coverage.xml`.
4. `4 Simulate Mundial + Static Site`: corre la simulacion, genera `dist/data/` y `dist/index.html`.
5. `5 Deploy GitHub Pages`: publica el sitio estatico en GitHub Pages.

## Diagnostico y fix del pipeline rojo

La primera ejecucion del pipeline fallo antes de correr los jobs porque GitHub no podia
parsear el archivo YAML. El error estaba en la variable:

```yaml
DATABASE_URL: sqlite:///:memory:
```

El valor contenia `:` y necesitaba estar entre comillas para ser YAML valido. El fix minimo fue:

```yaml
DATABASE_URL: "sqlite:///:memory:"
```

Luego se volvio a ejecutar el workflow y los 5 jobs finalizaron correctamente.

## Commits relevantes

- `e2015e5 add cicd pipeline`: agrega workflow, script de simulacion y soporte de base de datos en memoria.
- `85afe1d fix workflow yaml`: corrige el error de sintaxis YAML en `DATABASE_URL`.

## Texto corto para entregar

```text
Implemente el pipeline CI/CD del Simulador Mundial 2026 con GitHub Actions.

El workflow ejecuta 5 jobs encadenados:
1. Lint con Ruff.
2. Tests con cobertura.
3. Quality Gate con umbral minimo de 80%.
4. Simulacion del Mundial y generacion de sitio estatico en dist/.
5. Deploy a GitHub Pages.

Durante la ejecucion inicial el pipeline fallo por un error de sintaxis YAML en la variable DATABASE_URL. Diagnostique el fallo, aplique el fix minimo y volvi a ejecutar el pipeline hasta dejarlo verde.

Repositorio:
https://github.com/Melina510/ejercicio-alumnos

Run exitoso de GitHub Actions:
https://github.com/Melina510/ejercicio-alumnos/actions/runs/28205843911

Sitio publicado en GitHub Pages:
https://melina510.github.io/ejercicio-alumnos/
```

## Evidencias sugeridas

- Captura del workflow exitoso donde se vea `Success`.
- Captura del grafo con los 5 jobs verdes.
- Captura del sitio publicado en GitHub Pages con el campeon del Mundial.
