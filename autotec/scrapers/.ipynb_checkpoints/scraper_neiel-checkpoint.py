import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cierra procesos viejos que hayan quedado abiertos
os.system("pkill -9 chrome || true")
os.system("pkill -9 chromedriver || true")
os.system("rm -rf /tmp/.com.google.Chrome.*")
os.system("rm -rf /tmp/.org.chromium.Chromium.*")
print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Neiel"
    lista_autos = []
    driver = None

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--headless=new")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Navegador iniciado correctamente.")

        limite_paginas = 3
        driver.get("https://www.autocosmos.cl/auto/usado")

        for nivel_pagina in range(limite_paginas):
            print(f"--- Procesando Página {nivel_pagina + 1} ---")

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article.listing-card")
                )
            )

            bloques = driver.find_elements(By.CSS_SELECTOR, "article.listing-card")

            for bloque in bloques:
                try:
                    enlace = bloque.find_element(By.CSS_SELECTOR, "a")
                    nombre = enlace.get_attribute("title")
                    if not nombre:
                        nombre = enlace.text

                    precio_limpio = ""
                    try:
                        precio_elemento = bloque.find_element(
                            By.CSS_SELECTOR, "span[class*='price-value']"
                        )
                        try:
                            precio_limpio = precio_elemento.find_element(
                                By.TAG_NAME, "meta"
                            ).get_attribute("content")
                        except:
                            precio_limpio = precio_elemento.text
                    except:
                        precio_limpio = ""

                    precio_texto = str(precio_limpio).replace(".", "").replace(",", "").replace("$", "").strip()
                    try:
                        valor_final = float(precio_texto) if precio_texto else 0.0
                    except ValueError:
                        valor_final = 0.0

                    lista_autos.append({
                        "identificador": nombre.strip(),
                        "valor": valor_final,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    })

                except Exception:
                    continue

            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                btn_sig = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, "a.pagination__next, a[rel='next']")
                    )
                )

                driver.execute_script("arguments[0].click();", btn_sig)
                print(f"👉 Avanzando a la página {nivel_pagina + 2}...")
                time.sleep(5)

            except Exception:
                print("No se pudo avanzar más: ya es la última página o el botón cambió.")
                break

        print(f"✅ Extracción terminada: {len(lista_autos)} productos.")
        return lista_autos

    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
        return []

    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass
