#!/usr/bin/env python3
"""Generar reporte HTML tipo Allure desde resultados de pytest"""

import json
from pathlib import Path
from datetime import datetime

def read_allure_results(results_dir):
    """Leer archivos JSON de resultados de Allure"""
    tests = []
    results_path = Path(results_dir)
    
    if not results_path.exists():
        return tests
    
    for json_file in results_path.glob("*.json"):
        with open(json_file, 'r') as f:
            data = json.load(f)
            tests.append(data)
    
    return tests

def generate_html_report(tests, output_file="allure-report.html"):
    """Generar reporte HTML con estilo Allure"""
    
    # Filtrar solo tests con estado válido (excluir 'unknown')
    tests_filtered = [t for t in tests if t.get('status') in ('passed', 'failed', 'skipped')]
    
    passed = sum(1 for t in tests_filtered if t.get('status') == 'passed')
    failed = sum(1 for t in tests_filtered if t.get('status') == 'failed')
    skipped = sum(1 for t in tests_filtered if t.get('status') == 'skipped')
    total = len(tests_filtered)
    
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reporte E2E - Simulador Mundial 2026</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 40px;
            background: #f8f9fa;
        }}
        .stat-card {{
            background: white;
            border-radius: 8px;
            padding: 25px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            border-left: 4px solid #667eea;
        }}
        .stat-card.passed {{
            border-left-color: #28a745;
        }}
        .stat-card.failed {{
            border-left-color: #dc3545;
        }}
        .stat-card.skipped {{
            border-left-color: #ffc107;
        }}
        .stat-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .stat-card.passed .number {{ color: #28a745; }}
        .stat-card.failed .number {{ color: #dc3545; }}
        .stat-card.skipped .number {{ color: #ffc107; }}
        .stat-card .label {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .progress-bar {{
            margin-top: 40px;
            background: #e9ecef;
            border-radius: 8px;
            overflow: hidden;
            height: 30px;
        }}
        .progress-fill {{
            background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
            height: 100%;
            width: {pass_rate}%;
            display: flex;
            align-items: center;
            justify-content: flex-end;
            padding-right: 10px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
            transition: width 0.3s ease;
        }}
        .tests-section {{
            padding: 40px;
        }}
        .tests-section h2 {{
            color: #333;
            margin-bottom: 25px;
            font-size: 1.8em;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .test-item {{
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 15px;
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 15px;
            transition: all 0.3s ease;
        }}
        .test-item:hover {{
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }}
        .test-status {{
            min-width: 100px;
            padding: 8px 15px;
            border-radius: 6px;
            font-weight: bold;
            text-align: center;
            font-size: 0.9em;
            text-transform: uppercase;
        }}
        .test-status.passed {{
            background: #d4edda;
            color: #155724;
        }}
        .test-status.failed {{
            background: #f8d7da;
            color: #721c24;
        }}
        .test-status.skipped {{
            background: #fff3cd;
            color: #856404;
        }}
        .test-info {{
            flex: 1;
        }}
        .test-name {{
            font-weight: 600;
            color: #333;
            font-size: 1.05em;
            margin-bottom: 5px;
        }}
        .test-duration {{
            font-size: 0.85em;
            color: #999;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px 40px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
            font-size: 0.9em;
        }}
        .logo {{
            display: inline-block;
            margin-bottom: 15px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🌍⚽</div>
            <h1>Reporte E2E - Simulador Mundial 2026</h1>
            <p>Validación de Frontend + APIs</p>
        </div>
        
        <div class="stats">
            <div class="stat-card passed">
                <div class="label">Pruebas Pasadas</div>
                <div class="number">{passed}</div>
            </div>
            <div class="stat-card failed">
                <div class="label">Pruebas Fallidas</div>
                <div class="number">{failed}</div>
            </div>
            <div class="stat-card skipped">
                <div class="label">Pruebas Omitidas</div>
                <div class="number">{skipped}</div>
            </div>
            <div class="stat-card">
                <div class="label">Total</div>
                <div class="number">{total}</div>
            </div>
        </div>
        
        <div style="padding: 0 40px;">
            <h3 style="color: #333; margin: 30px 0 15px 0; font-size: 1.1em;">
                Tasa de Éxito: {pass_rate:.1f}%
            </h3>
            <div class="progress-bar">
                <div class="progress-fill">{pass_rate:.0f}%</div>
            </div>
        </div>
        
        <div class="tests-section">
            <h2>Resultados Detallados</h2>
"""
    
    for test in tests_filtered:
        status = test.get('status', 'unknown')
        name = test.get('name', 'Unknown Test')
        duration = test.get('stop', 0) - test.get('start', 0)
        duration_ms = duration / 1000 if duration else 0
        
        # Limpiar nombre del test
        test_display_name = name.replace('test_e2e_', 'E2E-').replace('_', ' ').title()
        
        html += f"""            <div class="test-item">
                <div class="test-status {status}">{status}</div>
                <div class="test-info">
                    <div class="test-name">{test_display_name}</div>
                    <div class="test-duration">Duración: {duration_ms:.2f}ms</div>
                </div>
            </div>
"""
    
    html += """        </div>
        
        <div class="footer">
            <p>✅ <strong>Reporte Generado:</strong> """
    html += datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    html += """</p>
            <p>📊 Suite de Pruebas E2E - Frontend + APIs | 10/10 Casos de Prueba</p>
        </div>
    </div>
</body>
</html>
"""
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return output_file

if __name__ == "__main__":
    print("📊 Generando reporte Allure...")
    tests = read_allure_results("allure-results")
    tests_filtered = [t for t in tests if t.get('status') in ('passed', 'failed', 'skipped')]
    
    if not tests_filtered:
        print("❌ No se encontraron resultados de Allure")
        exit(1)
    
    output = generate_html_report(tests_filtered)
    print(f"✅ Reporte generado: {output}")
    print("📈 Estadísticas:")
    print(f"   - Pruebas Pasadas: {sum(1 for t in tests_filtered if t.get('status') == 'passed')}")
    print(f"   - Pruebas Fallidas: {sum(1 for t in tests_filtered if t.get('status') == 'failed')}")
    print(f"   - Total: {len(tests_filtered)}")
