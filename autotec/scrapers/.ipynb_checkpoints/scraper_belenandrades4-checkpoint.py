#autoselect
import time
import re
import requests
from bs4 import BeautifulSoup

print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    }

    URL_BASE = "https://www.autoselect.cl/web/autos-usados?page={}"

    for nivel_pagina in range(1, 20):
        url_pagina = URL_BASE.format(nivel_pagina)

        try:
            response = requests.get(url_pagina, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, "lxml")
            items = soup.select("div.item.item-es")
            print(f"  -> {len(items)} autos encontrados.")

            if len(items) == 0:
                print("  Sin mas autos, fin de paginas.")
                break

            for item in items:
                try:
                    try:
                        url_auto = "https://www.autoselect.cl" + item.select_one("a.link-vehiculo, a[href*='/web/vehiculos/view']").get("href")
                    except:
                        url_auto = "N/A"

                    try:
                        marca_modelo = item.select_one("h3.brand").text.strip()
                        partes = marca_modelo.split(" ", 1)
                        marca  = partes[0] if len(partes) > 0 else "N/A"
                        modelo = partes[1] if len(partes) > 1 else "N/A"
                    except:
                        marca = modelo = "N/A"

                    try:
                        precio = item.select_one("span.price").text.strip()
                    except:
                        precio = "0"

                    try:
                        texto_features = item.get_text()

                        year_match = re.search(r'\b(19|20)\d{2}\b', texto_features)
                        year = year_match.group() if year_match else "N/A"

                        km_match = re.search(r'([\d\.]+)\s*KM', texto_features)
                        kilometraje = km_match.group(1) if km_match else "N/A"

                        combustible = "N/A"
                        for c in ["Gasolina", "Diesel", "Electrico", "Hibrido", "Bencina"]:
                            if c.lower() in texto_features.lower():
                                combustible = c
                                break
                    except:
                        year = kilometraje = combustible = "N/A"

                    lista_autos.append({
                        "marca":         marca,
                        "modelo":        modelo,
                        "year":          year,
                        "kilometraje":   kilometraje,
                        "combustible":   combustible,
                        "ciudad":        "Cerrillos, Santiago",
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

