import os
import re
import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NOMBRE_GRUPO = ""
USUARIO = ""


def limpiar_numero(texto):
    if not texto:
        return 0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0


def ejecutar_extraccion():
    lista_autos = []
    driver = None

    print("🧹 Cerrando procesos anteriores...")
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")
    os.system("rm -rf /tmp/.com.google.Chrome.*")
    os.system("rm -rf /tmp/.org.chromium.Chromium.*")
    print("✅ Limpieza lista.")

    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    try:
        print("🌐 Iniciando navegador...")
        driver = webdriver.Chrome(options=options)
        print("✅ Navegador iniciado.")
        limite_paginas=3
        url_inicial = "https://www.autocosmos.cl/auto/usado"
        driver.get(url_inicial)

        for nivel_pagina in range(limite_paginas):
            print(f"\n📄 Procesando página {nivel_pagina + 1}...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "article.listing-card"))
            )

            bloques = driver.find_elements(By.CSS_SELECTOR, "article.listing-card")

            for i, bloque in enumerate(bloques, start=1):
                try:
                    enlace = bloque.find_element(By.CSS_SELECTOR, "a")
                    url_auto = enlace.get_attribute("href")
                    nombre = enlace.get_attribute("title") or enlace.text

                    marca = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__brand").text.strip()
                    modelo = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__model").text.strip()

                    try:
                        version = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__version").text.strip()
                    except Exception:
                        version = ""

                    try:
                        anio = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__year").text.strip()
                    except Exception:
                        anio = ""

                    try:
                        kilometraje_txt = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__km").text.strip()
                        kilometraje = limpiar_numero(kilometraje_txt)
                    except Exception:
                        kilometraje = 0

                    version_lower = version.lower()
                    if "diesel" in version_lower or "diésel" in version_lower or "tdi" in version_lower or "hdi" in version_lower or "crdi" in version_lower:
                        combustible = "Diesel"
                    elif "electrico" in version_lower or "eléctrico" in version_lower or "ev" in version_lower:
                        combustible = "Eléctrico"
                    elif "hibrido" in version_lower or "híbrido" in version_lower or "hybrid" in version_lower:
                        combustible = "Híbrido"
                    elif "bencina" in version_lower or "gasolina" in version_lower:
                        combustible = "Bencina"
                    elif "gas" in version_lower or "gnc" in version_lower or "glp" in version_lower:
                        combustible = "Gas"
                    else:
                        combustible = "No especificado"

                    try:
                        ciudad = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__city").text.strip()
                        ciudad = ciudad.replace("|", "").strip()
                    except Exception:
                        ciudad = "No especificado"

                    try:
                        precio_elemento = bloque.find_element(By.CSS_SELECTOR, "span.listing-card__price-value")
                        precio_txt = precio_elemento.get_attribute("content") or precio_elemento.text
                    except Exception:
                        precio_txt = "0"

                    precio = limpiar_numero(precio_txt)

                    auto = {
                        "identificador": nombre.strip(),
                        "marca": marca,
                        "modelo": modelo,
                        "anio": limpiar_numero(anio),
                        "kilometraje": kilometraje,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": url_auto,
                        "precio": precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    }

                    lista_autos.append(auto)

                except Exception as e:
                    print(f"     ❌ Error en auto #{i}: {e}")
                    traceback.print_exc()
                    continue

            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                btn_sig = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination__next, a[rel='next']"))
                )
                driver.execute_script("arguments[0].click();", btn_sig)
                time.sleep(5)

            except Exception as e:
                print(f"⛔ No se pudo avanzar de página: {e}")
                break

    except Exception as e:
        print(f"❌ Error general en Selenium: {e}")
        traceback.print_exc()

    finally:
        if driver is not None:
            try:
                driver.quit()
                print("🛑 Navegador cerrado.")
            except Exception:
                pass

    return lista_autos