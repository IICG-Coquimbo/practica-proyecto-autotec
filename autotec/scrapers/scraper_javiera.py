import time
import re
from datetime import datetime
<<<<<<< HEAD
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuración Global --
NOMBRE_GRUPO = "AutoTec"
USUARIO = "Javiera"

def crear_driver():
    """Crea una nueva instancia del navegador Chrome"""
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)
    return driver, wait

def ejecutar_extraccion(max_paginas=45, reiniciar_cada=20):
    FECHA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    driver, wait = crear_driver()
    
    datos_base = []
    datos_finales = []
    urls_vistas = set()

    try:
        print(f"🚀 Iniciando Clicar (Javiera) para ~{max_paginas * 20} registros...")

        # FASE 1: Captura de URLs en el índice
        for pagina in range(1, max_paginas + 1):
            url = f"https://www.clicar.cl/vehiculos/usado?page={pagina}"
            try:
                driver.get(url)
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li.h-fit")))
                autos = driver.find_elements(By.CSS_SELECTOR, "li.h-fit")
                
                for auto in autos:
                    try:
                        link = auto.find_element(By.TAG_NAME, "a").get_attribute("href")
                        if link and link not in urls_vistas:
                            urls_vistas.add(link)
                            
                            # Info rápida de la tarjeta
                            texto_tarjeta = auto.text.strip()
                            precio_match = re.search(r"\$\s?([\d\.]+)", texto_tarjeta)
                            precio = precio_match.group(1).replace(".", "") if precio_match else "0"
                            try:
                                img = auto.find_element(By.CSS_SELECTOR, "img.object-cover")
                                foto_url = img.get_attribute("srcset") or img.get_attribute("src") or ""
                                
                                if foto_url and "," in foto_url:
                                    foto_url = foto_url.split(",")[-1].strip().split(" ")[0]
                            except Exception:
                                foto_url = ""

                            datos_base.append({
                                "url": link,
                                "precio": precio,
                                "fecha_captura": FECHA,
                                "foto_url": foto_url,
                                "grupo": NOMBRE_GRUPO,
                                "usuario": USUARIO
                            })
                    except: continue
            except Exception as e:
                print(f"  ⚠️ Salto en página {pagina} por error.")
                continue

        # FASE 2: Extracción de detalles con REINICIO DE MEMORIA
        print(f"🔎 Fase 1 lista. Total URLs base: {len(datos_base)}")
        for i, dato in enumerate(datos_base, start=1):
            # Lógica de reinicio para liberar RAM
            if i % reiniciar_cada == 0:
                driver.quit()
                driver, wait = crear_driver()

            try:
                driver.get(dato["url"])
                time.sleep(1.5)
                cuerpo = driver.find_element(By.TAG_NAME, "body").text.lower()

                # Extraer Marca/Modelo de la URL (más confiable en Clicar)
                # URL tipo: .../venta/chevrolet/onix/12345
                partes_url = dato["url"].split("/")
                dato["marca"] = partes_url[-3].title() if len(partes_url) > 3 else "N/A"
                dato["modelo"] = partes_url[-2].title() if len(partes_url) > 2 else "N/A"

                # Año
                year_match = re.search(r"\b(20\d{2}|19\d{2})\b", cuerpo)
                dato["year"] = year_match.group(1) if year_match else "0"
                
                # Kilometraje
                km_match = re.search(r"(\d[\d\.]*)\s*km", cuerpo)
                dato["kilometraje"] = km_match.group(1).replace(".", "") if km_match else "0"

                # Combustible
                if "gasolina" in cuerpo or "bencina" in cuerpo: dato["combustible"] = "Gasolina"
                elif "diesel" in cuerpo or "diésel" in cuerpo: dato["combustible"] = "Diesel"
                else: dato["combustible"] = "N/A"

                dato["ciudad"] = "N/A"
                datos_finales.append(dato)
                if i % 10 == 0:
                    print(f"  Detalles procesados: {i}/{len(datos_base)}")
            except:
                continue

    finally:
        driver.quit()
        print(f"🔒 Proceso de Javiera terminado. Total: {len(datos_finales)}")
=======
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def ejecutar_extraccion(max_paginas=50):
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    NOMBRE = "Javiera Pizarro"
    FECHA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos_base = []
    datos_finales = []

    for pagina in range(1, max_paginas + 1):
        url = f"https://www.clicar.cl/vehiculos/usado?page={pagina}"
        driver.get(url)
        time.sleep(5)

        autos = driver.find_elements(By.CSS_SELECTOR, "li.h-fit")

        for auto in autos:
            try:
                texto = auto.text.strip()
                lineas = [x.strip() for x in texto.split("\n") if x.strip()]
                link = auto.find_element(By.TAG_NAME, "a").get_attribute("href")

                partes_url = link.split("/marcas/")[1].split("/")
                marca = partes_url[0].replace("-", " ").title()

                slug = partes_url[2]
                slug = re.sub(r"-\d+$", "", slug)
                slug = slug.replace(partes_url[0] + "-", "")
                modelo = slug.replace("-", " ").title()

                texto_completo = " ".join(lineas)

                match_year = re.search(r"\b(20\d{2})\b", texto_completo)
                year = match_year.group(1) if match_year else None

                match_km = re.search(r"(\d{1,3}(?:\.\d{3})*)\s*Km", texto_completo, re.IGNORECASE)
                kilometraje = match_km.group(1) + " Km" if match_km else None

                precio = None
                for i, linea in enumerate(lineas):
                    if linea == "$" and i + 1 < len(lineas):
                        precio = "$" + lineas[i + 1]
                        break

                datos_base.append({
                    "marca": marca,
                    "modelo": modelo,
                    "year": year,
                    "kilometraje": kilometraje,
                    "combustible": "No especificado",
                    "ciudad": "No disponible",
                    "url": link,
                    "precio": precio,
                    "nombre": NOMBRE,
                    "fecha_captura": FECHA
                })

            except Exception:
                continue

    for dato in datos_base:
        try:
            driver.get(dato["url"])
            time.sleep(2)

            texto_original = driver.find_element(By.TAG_NAME, "body").text
            texto = texto_original.lower()

            ciudad = "No disponible"
            for linea in texto_original.split("\n"):
                if "," in linea and "vehículo" not in linea.lower():
                    posible_ciudad = linea.split(",")[-1].strip()
                    if 2 < len(posible_ciudad) < 40:
                        ciudad = posible_ciudad
                        break

            if "gasolina" in texto:
                combustible = "Gasolina"
            elif "diesel" in texto or "diésel" in texto:
                combustible = "Diesel"
            elif "híbrido" in texto or "hibrido" in texto:
                combustible = "Híbrido"
            elif "eléctrico" in texto or "electrico" in texto:
                combustible = "Eléctrico"
            elif "petróleo" in texto or "petroleo" in texto:
                combustible = "Petróleo"
            else:
                combustible = "No especificado"

            dato["ciudad"] = ciudad
            dato["combustible"] = combustible

            datos_finales.append(dato)

        except Exception:
            datos_finales.append(dato)

    driver.quit()

    client = MongoClient("mongodb://mongodb:27017/")
    db = client["proyecto_bigdata"]
    coleccion = db["datos_scraping"]

    for dato in datos_finales:
        coleccion.update_one(
            {"url": dato["url"]},
            {"$set": dato},
            upsert=True
        )

    print("🔥 LISTO")
    print("📦 Total:", len(datos_finales))
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25

    return datos_finales