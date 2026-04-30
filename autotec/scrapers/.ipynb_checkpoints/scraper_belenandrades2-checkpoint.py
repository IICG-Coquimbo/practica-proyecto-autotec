import os
import time
import json
import requests
from bs4 import BeautifulSoup

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []

    # Usamos headers para evitar bloqueos básicos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    limite_paginas = 5  # Reducido para pruebas rápidas, puedes subirlo a 20
    URL_BASE = "https://gildemeisterusados.cl/page/{}/"

    print(f"🚀 Iniciando extracción en Gildemeister para el grupo {NOMBRE_GRUPO}")

    for nivel_pagina in range(1, limite_paginas + 1):
        url_pagina = URL_BASE.format(nivel_pagina)

        try:
            response = requests.get(url_pagina, headers=headers, timeout=10)
            
            # CAMBIO AQUÍ: Usamos html.parser en lugar de lxml para evitar el error de librería faltante
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Gildemeister usa etiquetas <article class="card--vehicle">
            articles = soup.select("article.card--vehicle")

            if not articles:
                print(f"⚠️ No se encontraron artículos en la página {nivel_pagina}")
                break

            for article in articles:
                try:
                    # Buscamos el atributo :item que contiene el JSON con la info
                    item_tag = article.select_one("[\\:item]")
                    if not item_tag:
                        continue

                    # El contenido está en formato JSON dentro del atributo
                    item_json = json.loads(item_tag[":item"])

                    # Extracción de datos desde el JSON
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

            print(f"✅ Página {nivel_pagina} procesada. Acumulado: {len(lista_autos)} autos.")
            time.sleep(1)

        except Exception as e:
            print(f"❌ Error en página {nivel_pagina}: {e}")
            continue

    print(f"\n✨ Extracción de Gildemeister terminada: {len(lista_autos)} autos capturados.")
    return lista_autos