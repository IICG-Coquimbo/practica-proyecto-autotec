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
    print("Navegador iniciado correctamente.")

    try:
        limite_paginas = 3

        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = f"{URL_BASE}{nivel_pagina}/"
            print(f"Procesando Página {nivel_pagina}")
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
                    bloque = tarjeta.find_element(By.CSS_SELECTOR, "div.title.heading-font a.rmv_txt_drctn")
                    url = bloque.get_attribute("href")

                    valores = tarjeta.find_elements(By.CSS_SELECTOR, "div.value")
                    marca = modelo = anio = kilometraje = combustible = transmision = ""

                    for v in valores:
                        texto = v.text.strip().upper()
                        if "KM" in texto or "KMS" in texto:
                            kilometraje = texto
                        elif texto.isdigit() and len(texto) == 4:
                            anio = texto
                        elif texto in ["GASOLINA", "DIESEL", "HIBRIDO"]:
                            combustible = texto
                        elif texto in ["MECANICO", "AUTOMATICO"]:
                            transmision = texto
                        else:
                            if not marca:
                                marca = texto
                            elif not modelo:
                                modelo = texto

                    try:
                        ciudad_elemento = tarjeta.find_element(By.CSS_SELECTOR, "div.stm-tooltip-link")
                        ciudad = ciudad_elemento.text.strip()
                    except:
                        ciudad = ""

                    precio_elementos = tarjeta.find_elements(By.CSS_SELECTOR, "span.heading-font")
                    precio = precio_elementos[0].text.strip() if precio_elementos else "Consultar"

                    precio_limpio = re.sub(r'\D', '', precio)
                    km_limpio = re.sub(r'\D', '', kilometraje)

                    lista_autos.append({
                        "marca": marca,
                        "modelo": modelo,
                        "anio": anio,
                        "kilometraje": int(km_limpio) if km_limpio else 0,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": url,
                        "precio": float(precio_limpio) if precio_limpio else 0.0,
                        "usuario": "Martin",
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": "AutoTec"
                    })

                except Exception:
                    continue

        print(f"Extracción terminada: {len(lista_autos)} vehículos.")
        return lista_autos

    except Exception as e:
        print(f"Error en Selenium: {e}")
        return []

    finally:
        driver.quit()