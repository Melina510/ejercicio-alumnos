import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


DIST_DIR = Path("dist")
DATA_DIR = DIST_DIR / "data"


def write_json(name: str, payload: object) -> None:
    path = DATA_DIR / name
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )


def render_static_page(simulation: dict, metrics: dict, teams: list[dict]) -> str:
    embedded = json.dumps(
        {"simulation": simulation, "metrics": metrics, "teams": teams},
        ensure_ascii=False,
    )
    champion = simulation["champion"]
    top_scorer = metrics["top_scorer"]
    groups_html = "\n".join(
        f"""
        <section class="group">
          <h2>Grupo {group["group"]}</h2>
          <ol>
            {''.join(f'<li><strong>{team["team"]}</strong> - {team["pts"]} pts, DG {team["gd"]:+d}</li>' for team in group["standings"])}
          </ol>
        </section>
        """
        for group in simulation["groups"]
    )
    final = simulation["final"]
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Simulador Mundial 2026</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f5f7fb; color: #172033; }}
    header {{ background: #0056a7; color: white; padding: 32px 24px; text-align: center; }}
    main {{ max-width: 1100px; margin: 0 auto; padding: 24px; }}
    .summary {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 24px 0; }}
    .card, .group {{ background: white; border: 1px solid #d9e2ef; border-radius: 8px; padding: 16px; }}
    .groups {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }}
    h1, h2, p {{ margin-top: 0; }}
    code {{ display: block; white-space: pre-wrap; word-break: break-word; background: #edf2f7; padding: 12px; border-radius: 6px; }}
  </style>
</head>
<body>
  <header>
    <h1>Campeon del Mundo 2026: {champion}</h1>
    <p>Sitio estatico generado durante GitHub Actions, sin backend en produccion.</p>
  </header>
  <main>
    <section class="summary">
      <div class="card"><h2>Final</h2><p>{final["home_team"]} {final["home_goals"]} - {final["away_goals"]} {final["away_team"]}</p></div>
      <div class="card"><h2>Goleador</h2><p>{top_scorer["player_name"]} ({top_scorer["team_name"]}) - {top_scorer["goals"]} goles</p></div>
      <div class="card"><h2>Goles</h2><p>{metrics["total_goals"]} en {metrics["total_matches"]} partidos</p></div>
      <div class="card"><h2>Equipos</h2><p>{len(teams)} clasificados simulados</p></div>
    </section>
    <section class="groups">
      {groups_html}
    </section>
    <h2>Datos embebidos</h2>
    <code id="payload"></code>
  </main>
  <script>
    window.__WORLD_CUP_DATA__ = {embedded};
    document.getElementById("payload").textContent = JSON.stringify(window.__WORLD_CUP_DATA__, null, 2);
  </script>
</body>
</html>
"""


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with TestClient(app) as client:
        simulation = client.post("/simulator/run").json()
        metrics = client.get("/metrics/dashboard").json()
        teams = client.get("/teams/").json()

    write_json("simulation.json", simulation)
    write_json("metrics.json", metrics)
    write_json("teams.json", teams)
    (DIST_DIR / "index.html").write_text(
        render_static_page(simulation, metrics, teams),
        encoding="utf-8",
    )

    print(f"Campeon del mundo: {simulation['champion']}")
    print("Sitio estatico generado en dist/index.html")


if __name__ == "__main__":
    main()
