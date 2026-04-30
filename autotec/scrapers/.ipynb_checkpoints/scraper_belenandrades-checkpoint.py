#callegari
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

os.system("pkill -9 chrome")
os.system("pkill -9 chromedriver")
os.system("rm -rf /tmp/.com.google.Chrome.*")
os.system("rm -rf /tmp/.org.chromium.Chromium.*")
print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []
    driver = None

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    try:
        driver = uc.Chrome(options=options, version_main=147)
        print("Navegador iniciado correctamente.")

        limite_paginas = 10
        URL_BASE = "https://callegari.cl/seminuevos/page/{}"

        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = URL_BASE.format(nivel_pagina)

            driver.get(url_pagina)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)

            bloques = driver.find_elements(By.CSS_SELECTOR, "a.auto-block")

            for bloque in bloques:
                try:
                    url_auto = bloque.get_attribute("href")

                    # Extraemos todo el texto y separamos por lineas
                    lineas = [l.strip() for l in bloque.text.strip().split("\n") if l.strip()]

                    # Detectar si hay badge en la primera linea
                    badges = ["Auto Empresa", "Garantia Fabrica", "Garantía Fábrica", "Unico Dueno", "Único Dueño"]
                    inicio = 1 if any(b.lower() in lineas[0].lower() for b in badges) else 0

                    marca  = lineas[inicio + 0] if len(lineas) > inicio + 0 else "N/A"
                    modelo = lineas[inicio + 1] if len(lineas) > inicio + 1 else "N/A"
                    precio = lineas[inicio + 3] if len(lineas) > inicio + 3 else "0"

                    if len(lineas) > inicio + 4:
                        partes      = [p.strip() for p in lineas[inicio + 4].split("|")]
                        year        = partes[0] if len(partes) > 0 else "N/A"
                        kilometraje = partes[1] if len(partes) > 1 else "N/A"
                        combustible = partes[3] if len(partes) > 3 else "N/A"
                    else:
                        year = kilometraje = combustible = "N/A"
    
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

            time.sleep(2)

        print(f"Extraccion terminada: {len(lista_autos)} autos en total.")
        return lista_autos

    except Exception as e:
        print(f"Error en Selenium: {e}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass



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
        time.sleep(1)

    print(f"\nExtraccion terminada: {len(lista_autos)} autos en total.")
    return lista_autos




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



#valentini
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

os.system("pkill -9 chrome")
os.system("pkill -9 chromedriver")
os.system("rm -rf /tmp/.com.google.Chrome.*")
os.system("rm -rf /tmp/.org.chromium.Chromium.*")
print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []
    driver = None

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    try:

        driver = uc.Chrome(options=options, version_main=147)

        limite_paginas = 5

        URL_BASE = "https://seminuevosvalentini.cl/search/page/{}/"

        for pagina in range(1, limite_paginas + 1):

            url = URL_BASE.format(pagina)

            driver.get(url)

            time.sleep(5)

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(3)

            # BLOQUES DE AUTOS
            bloques = driver.find_elements(
                By.CSS_SELECTOR,
                "div.vehica-car-card__content"
            )


            for bloque in bloques:

                try:

                    # NOMBRE + URL
                    nombre_elemento = bloque.find_element(
                        By.CSS_SELECTOR,
                        "a.vehica-car-card__name"
                    )

                    nombre = nombre_elemento.text.strip()

                    url_auto = nombre_elemento.get_attribute("href")

                    # PRECIO
                    try:
                        precio = bloque.find_element(
                            By.CSS_SELECTOR,
                            "div.vehica-car-card__price"
                        ).text.strip()
                    except:
                        precio = 0

                    # INFORMACION EXTRA
                    infos = bloque.find_elements(
                        By.CSS_SELECTOR,
                        "div.vehica-car-card__info__single"
                    )

                    year = infos[0].text if len(infos) > 0 else 0
                    kilometraje = infos[1].text if len(infos) > 1 else 0
                    combustible = infos[3].text if len(infos) > 3 else "N/A"

                    # SEPARAR MARCA Y MODELO
                    partes_nombre = nombre.split(" ", 1)

                    marca = (
                        partes_nombre[0]
                        if len(partes_nombre) > 0
                        else "N/A"
                    )

                    modelo = (
                        partes_nombre[1]
                        if len(partes_nombre) > 1
                        else "N/A"
                    )

                    # GUARDAR DATOS
                    lista_autos.append({

                        "marca": marca if marca else "N/A",

                        "modelo": modelo if modelo else "N/A",

                        "year": year if year else 0,

                        "kilometraje": kilometraje if kilometraje else 0,

                        "combustible": combustible if combustible else "N/A",

                        "ciudad": "N/A",

                        "url": url_auto if url_auto else "N/A",

                        "precio": precio if precio else 0,

                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),

                        "grupo": NOMBRE_GRUPO,

                        "usuario": USUARIO

                    })

                except Exception as e:

                    continue

            print(f"Acumulado total: {len(lista_autos)} autos")
            return lista_autos

    except Exception as e:

        print(f"Error Selenium: {e}")

    finally:

        if driver is not None:

            try:
                driver.quit()
            except:
                pass
