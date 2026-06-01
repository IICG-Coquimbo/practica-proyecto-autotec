import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuración Global ---
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

    return datos_finales