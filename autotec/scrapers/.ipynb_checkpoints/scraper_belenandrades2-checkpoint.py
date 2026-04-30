#gildemeister
import os
import time
import json
import requests
from bs4 import BeautifulSoup

print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []
    driver = None

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    limite_paginas = 20
    URL_BASE = "https://gildemeisterusados.cl/page/{}/"

    for nivel_pagina in range(1, limite_paginas + 1):
        url_pagina = URL_BASE.format(nivel_pagina)

        try:
            response = requests.get(url_pagina, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "lxml")
            articles = soup.select("article.card--vehicle")

            for article in articles:
                try:
                    item_tag = article.select_one("[\\:item]")
                    if not item_tag:
                        continue

                    item_json = json.loads(item_tag[":item"])

                    url_auto    = item_json.get("cta_vehicle", {}).get("url", "N/A")
                    marca       = item_json.get("brand", "N/A")
                    modelo      = item_json.get("subtitle", "N/A")
                    details     = item_json.get("details", {})
                    year        = details.get("year", "N/A")
                    kilometraje = details.get("mileage", "N/A")
                    combustible = details.get("fuel", "N/A")
                    precio      = item_json.get("pricing_details", {}).get("counted_price", {}).get("value", "0")

                    lista_autos.append({
                        "marca":         marca,
                        "modelo":        modelo,
                        "year":          year,
                        "kilometraje":   kilometraje,
                        "combustible":   combustible,
                        "ciudad":        "N/A",
                        "url":           url_auto,
                        "precio":        precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo":         NOMBRE_GRUPO,
                        "usuario":       USUARIO
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"  Error en pagina {nivel_pagina}: {e}")
            continue

        print(f"  Acumulado total: {len(lista_autos)} autos.")
        time.sleep(1)

    print(f"\nExtraccion terminada: {len(lista_autos)} autos en total.")
    return lista_autos
