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

NOMBRE_GRUPO = "AutoTec"
USUARIO = "Martin"

def limpiar_numero(texto):
    if not texto:
        return 0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0

def ejecutar_extraccion(limite_paginas=1):
    URL_BASE = "https://www.difor.cl/autos-usados-chile?page="
    lista_autos = []

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = f"{URL_BASE}{nivel_pagina}"
            driver.get(url_pagina)

            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@id='product-card-link']"))
            )

            tarjetas = driver.find_elements(By.XPATH, "//a[@id='product-card-link']")

            for tarjeta in tarjetas:
                try:
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
                        titulo = "No especificado"
                        marca = modelo = "No especificado"
                        year = 0

                    # Precio
                    try:
                        precio_txt = tarjeta.find_element(By.XPATH, ".//p[contains(@class,'MuiTypography-body2')]").text.strip()
                        precio = limpiar_numero(precio_txt)
                    except:
                        precio = 0

                    # Bloque de detalles (solo km y combustible)
                    kilometraje = 0
                    combustible = "No especificado"
                    try:
                        spans = tarjeta.find_elements(
                            By.XPATH,
                            ".//div[contains(@class,'MuiBox-root') and contains(@class,'css-dmamo3')]//span"
                        )
                        for s in spans:
                            texto = s.text.strip().upper()
                            if "KM" in texto or "KMS" in texto:
                                kilometraje = limpiar_numero(s.text)
                            elif any(x in texto for x in ["DIESEL","DIÉSEL","TDI","HDI","CRDI"]):
                                combustible = "Diesel"
                            elif any(x in texto for x in ["ELECTRICO","ELÉCTRICO","EV"]):
                                combustible = "Eléctrico"
                            elif any(x in texto for x in ["HIBRIDO","HÍBRIDO","HYBRID"]):
                                combustible = "Híbrido"
                            elif any(x in texto for x in ["BENCINA","GASOLINA"]):
                                combustible = "Bencina"
                            elif any(x in texto for x in ["GAS","GNC","GLP"]):
                                combustible = "Gas"
                    except:
                        pass

                    auto = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": kilometraje,
                        "combustible": combustible,
                        "ciudad": "No especificado",  # Difor no muestra ciudad en el card
                        "url": url_auto,
                        "precio": precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    }

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











