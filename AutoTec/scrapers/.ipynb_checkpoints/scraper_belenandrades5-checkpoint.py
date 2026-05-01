import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# =========================
# CONFIGURACIÓN PROYECTO
# =========================
NOMBRE_GRUPO = "AutoTec"
USUARIO = "Belen A"

def ejecutar_extraccion(max_paginas=5):
    # Limpieza de procesos para evitar saturación de memoria
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    # Añadimos un User-Agent real para evitar bloqueos básicos
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(options=options)
    lista_autos = []
    autos_vistos = set()

    URL_BASE = "https://www.salazarisrael.cl/vehiculos/usado?page={}"

    try:
        for pagina in range(1, max_paginas + 1):
            print(f"🔎 [Salazar Israel] Extrayendo página {pagina}...")
            driver.get(URL_BASE.format(pagina))
            time.sleep(5) # Tiempo para carga de JavaScript

            autos = driver.find_elements(By.CSS_SELECTOR, "article")
            if not autos:
                break

            for auto in autos:
                try:
                    texto = auto.text.strip()
                    if len(texto) < 20: continue

                    # Extraer URL para el Identificador Único
                    try:
                        link = auto.find_element(By.TAG_NAME, "a")
                        url_auto = link.get_attribute("href")
                    except:
                        continue

                    if not url_auto or url_auto in autos_vistos:
                        continue
                    
                    autos_vistos.add(url_auto)

                    # --- Lógica de procesamiento de texto ---
                    lineas = [l.strip() for l in texto.split("\n") if l.strip()]
                    
                    # Buscamos la línea que contiene el año y km (ej: "2022 | 15.000 Km")
                    detalle = next((l for l in lineas if "|" in l and "Km" in l), "")
                    if not detalle: continue

                    # Filtrar líneas para marca y modelo
                    lineas_utiles = [
                        l for l in lineas 
                        if "$" not in l and "Cuota" not in l and "RESERVAR" not in l 
                        and "COTIZAR" not in l and "VER MÁS" not in l and "|" not in l 
                        and "Km" not in l and len(l.strip()) > 1
                    ]

                    marca = lineas_utiles[0] if len(lineas_utiles) > 0 else "N/A"
                    modelo = " ".join(lineas_utiles[1:3]) if len(lineas_utiles) >= 2 else "N/A"

                    # Regex para limpiar datos
                    year_match = re.search(r'\b(19|20)\d{2}\b', detalle)
                    year = int(year_match.group()) if year_match else None

                    km_match = re.search(r'([\d\.]+)\s*Km', detalle)
                    km_texto = km_match.group(1).replace(".", "") if km_match else "0"
                    
                    # Precio: buscamos el símbolo $ y tomamos el siguiente valor
                    precio_final = 0
                    for i, l in enumerate(lineas):
                        if l == "$" and i + 1 < len(lineas):
                            precio_texto = re.sub(r"[^\d]", "", lineas[i+1])
                            precio_final = int(precio_texto) if precio_texto else 0
                            break

                    if not year or precio_final == 0:
                        continue

                    lista_autos.append({
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": int(km_texto),
                        "url": url_auto,
                        "precio": precio_final,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO,
                        "fuente": "salazarisrael.cl"
                    })

                except Exception:
                    continue

    finally:
        driver.quit()

    print(f"✅ Finalizado: {len(lista_autos)} autos capturados.")
    return lista_autos