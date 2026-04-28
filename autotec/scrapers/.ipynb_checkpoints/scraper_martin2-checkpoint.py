import sys
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

def ejecutar_extraccion(limite_paginas=35):  # 👈 por defecto 24 páginas
    URL_BASE = "https://www.difor.cl/autos-usados-chile?page="
    lista_autos = []
    vistos = set()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for nivel_pagina in range(1, limite_paginas + 1):
            print(f"📄 Procesando Página {nivel_pagina}")
            url_pagina = f"{URL_BASE}{nivel_pagina}"
            driver.get(url_pagina)

            # Esperar a que aparezcan los enlaces de autos
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@id='product-card-link']"))
            )

            tarjetas = driver.find_elements(By.XPATH, "//a[@id='product-card-link']")

            for tarjeta in tarjetas:
                try:
                    # URL única del auto
                    href = tarjeta.get_attribute("href")
                    url_auto = "https://www.difor.cl" + href if href.startswith("/") else href

                    # Marca, modelo, year
                    try:
                        titulo = tarjeta.find_element(By.XPATH, ".//p[contains(@class,'MuiTypography-body1')]").text.strip()
                        partes = titulo.split()
                        marca = partes[0] if len(partes) > 0 else "No especificado"
                        modelo = " ".join(partes[1:-1]) if len(partes) > 2 else "No especificado"
                        year = limpiar_numero(partes[-1]) if partes and partes[-1].isdigit() else 0
                    except:
                        marca = modelo = "No especificado"
                        year = 0

                    # Precio final (primer bloque body2, ignorando bono)
                    try:
                        precio_txt = tarjeta.find_element(By.XPATH, ".//p[contains(@class,'MuiTypography-body2')]").text.strip()
                        precio = limpiar_numero(precio_txt)
                    except:
                        precio = 0

                    # Bloque de detalles (km, transmisión, combustible)
                    kilometraje = 0
                    transmision = "No especificado"
                    combustible = "No especificado"
                    try:
                        spans = tarjeta.find_elements(By.XPATH, ".//div[contains(@class,'MuiBox-root') and contains(@class,'css-dmamo3')]/span")
                        for sp in spans:
                            txt = sp.text.strip()
                            if "km" in txt.lower():
                                kilometraje = limpiar_numero(txt)
                            elif "mecánica" in txt.lower() or "automática" in txt.lower():
                                transmision = txt
                            elif any(c in txt.lower() for c in ["gasolina", "diesel", "híbrido", "hibrido", "eléctrico", "electrico"]):
                                combustible = txt
                    except:
                        pass

                    ciudad = "No especificado"

                    identificador = f"{marca} {modelo}" if marca != "No especificado" and modelo != "No especificado" else "No especificado"

                    auto = {
                        "identificador": identificador,
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,  # 👈 cambiado de anio a year
                        "kilometraje": kilometraje,
                        "transmision": transmision,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": url_auto,
                        "precio": precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO,
                        "fuente": "Difor.cl"
                    }

                    # Guardar evitando duplicados
                    if auto["marca"] != "No especificado" and auto["modelo"] != "No especificado":
                        clave = (auto["identificador"], auto["year"], auto["kilometraje"])
                        if clave not in vistos:
                            vistos.add(clave)
                            lista_autos.append(auto)

                except:
                    continue

        return lista_autos

    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
        return []

    finally:
        driver.quit()










