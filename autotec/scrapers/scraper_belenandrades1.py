import os
import time
import re
from selenium import webdriver # Faltaba este import
from selenium.webdriver.chrome.options import Options # Faltaba este import
from selenium.webdriver.common.by import By

# =========================
# LIMPIEZA (Fuera de la función para que corra al importar)
# =========================
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

    # Configuración de opciones (Asegúrate de que coincida con tu entorno Docker)
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    # Agregamos un User-Agent para que Callegari no nos bloquee tan rápido
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    try:
        # IMPORTANTE: Aquí es donde daba el error. Usamos webdriver.Chrome estándar.
        driver = webdriver.Chrome(options=options)
        print("Navegador iniciado correctamente para Callegari.")

        limite_paginas = 10 # Bajamos el límite para pruebas, luego puedes subirlo a 10
        URL_BASE = "https://callegari.cl/seminuevos/page/{}"

        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = URL_BASE.format(nivel_pagina)

            try:
                driver.get(url_pagina)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(6)

                bloques = driver.find_elements(By.CSS_SELECTOR, "a.auto-block")

                for bloque in bloques:
                    try:
                        url_auto = bloque.get_attribute("href")
                        lineas = [l.strip() for l in bloque.text.strip().split("\n") if l.strip()]

                        if not lineas: continue

                        # Lógica de detección de badges
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

                        try:
                            div_imagen = bloque.find_element(By.CSS_SELECTOR, "div.u-img")
                            style_img = div_imagen.get_attribute("style")
                        
                            match = re.search(r'url\(["\']?(.*?)["\']?\)', style_img)
                            foto_url = match.group(1) if match else ""
                        except Exception:
                            foto_url = ""
                        
                        lista_autos.append({
                            "marca":         marca,
                            "modelo":        modelo,
                            "year":          year,
                            "kilometraje":   kilometraje,
                            "combustible":   combustible,
                            "ciudad":        "N/A",
                            "url":           url_auto,
                            "precio":        precio,
                            "foto_url":      foto_url,
                            "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "grupo":         NOMBRE_GRUPO,
                            "usuario":       USUARIO
                        })

                    except Exception:
                        continue

                time.sleep(2)
            
            except Exception as e:
                print(f"Error cargando página {nivel_pagina}: {e}")
                continue

        return lista_autos

    except Exception as e:
        print(f"Error en Selenium (Callegari): {e}")
        return []

    finally:
        if driver is not None:
            print("Cerrando navegador Callegari...")
            driver.quit()