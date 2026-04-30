import os
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient

NOMBRE_GRUPO = "AutoTec"
USUARIO = "Martin"

def limpiar_numero(texto):
    if not texto:
        return 0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0

def ejecutar_extraccion():
    URL_BASE = "https://seminuevos.aspillagahornauer.cl/stock-seminuevos/page/"
    lista_autos = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("🌐 Navegador iniciado correctamente.")

    try:
        limite_paginas = 8  # 👈 ahora recorre 8 páginas

        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = f"{URL_BASE}{nivel_pagina}/"
            print(f"📄 Procesando Página {nivel_pagina}")
            driver.get(url_pagina)
            time.sleep(5)

            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                    "div.listing-list-loop.stm-listing-directory-list-loop.stm-isotope-listing-item"))
            )

            tarjetas = driver.find_elements(By.CSS_SELECTOR,
                "div.listing-list-loop.stm-listing-directory-list-loop.stm-isotope-listing-item")

            for tarjeta in tarjetas:
                try:
                    enlace = tarjeta.find_element(By.CSS_SELECTOR, "div.title.heading-font a.rmv_txt_drctn")
                    url_auto = enlace.get_attribute("href")

                    valores = tarjeta.find_elements(By.CSS_SELECTOR, "div.value")
                    marca = modelo = year = kilometraje_txt = combustible = ""

                    for v in valores:
                        texto = v.text.strip()
                        texto_upper = texto.upper()
                        if "KM" in texto_upper or "KMS" in texto_upper:
                            kilometraje_txt = texto
                        elif texto.isdigit() and len(texto) == 4:
                            year = texto
                        elif any(x in texto_upper for x in ["DIESEL", "DIÉSEL", "TDI", "HDI", "CRDI"]):
                            combustible = "Diesel"
                        elif any(x in texto_upper for x in ["ELECTRICO", "ELÉCTRICO", "EV"]):
                            combustible = "Eléctrico"
                        elif any(x in texto_upper for x in ["HIBRIDO", "HÍBRIDO", "HYBRID"]):
                            combustible = "Híbrido"
                        elif any(x in texto_upper for x in ["BENCINA", "GASOLINA"]):
                            combustible = "Bencina"
                        elif any(x in texto_upper for x in ["GAS", "GNC", "GLP"]):
                            combustible = "Gas"
                        else:
                            if not marca:
                                marca = texto
                            elif not modelo:
                                modelo = texto

                    try:
                        ciudad_elemento = tarjeta.find_element(By.CSS_SELECTOR, "div.stm-tooltip-link")
                        ciudad = ciudad_elemento.text.strip()
                    except:
                        ciudad = "No especificado"

                    precio_elementos = tarjeta.find_elements(By.CSS_SELECTOR, "span.heading-font")
                    precio_txt = precio_elementos[0].text.strip() if precio_elementos else "0"

                    auto = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": limpiar_numero(year),
                        "kilometraje": limpiar_numero(kilometraje_txt),
                        "combustible": combustible if combustible else "No especificado",
                        "ciudad": ciudad,
                        "url": url_auto,
                        "precio": limpiar_numero(precio_txt),
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    }

                    print(auto)   # 👈 muestra cada auto en consola
                    lista_autos.append(auto)

                except Exception:
                    continue

        print(f"✅ Extracción terminada: {len(lista_autos)} vehículos.")
        return lista_autos

    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
        return []

    finally:
        driver.quit()






