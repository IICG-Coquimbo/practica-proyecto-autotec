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
                        anio        = partes[0] if len(partes) > 0 else "N/A"
                        kilometraje = partes[1] if len(partes) > 1 else "N/A"
                        combustible = partes[3] if len(partes) > 3 else "N/A"
                    else:
                        anio = kilometraje = combustible = "N/A"
    
                    lista_autos.append({
                        "marca":         marca,
                        "modelo":        modelo,
                        "anio":          anio,
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

            print(f"  Acumulado total: {len(lista_autos)} autos.")
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
