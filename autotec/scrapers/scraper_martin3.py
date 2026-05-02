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
    URL_BASE = "https://www.piamonteusados.cl/autos/seminuevos?annio_desde=&annio_hasta=&precios=&unidades=30"
    lista_autos = []
    urls_vistas = set()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("🌐 Empezó extracción en Piamonte Usados")

    try:
        driver.get(URL_BASE)

        # Esperar a que aparezcan tarjetas
        WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.shadow-sm.card-index.h-100.bg-card"))
        )

        autos_previos = 0
        for i in range(1):  # 👈 límite de scrolls (1)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)

            tarjetas = driver.find_elements(By.CSS_SELECTOR, "div.shadow-sm.card-index.h-100.bg-card")
            cantidad_actual = len(tarjetas)
            print(f"📄 Scroll {i+1}: {cantidad_actual} autos capturados")

            if cantidad_actual == autos_previos:
                print("🚫 No se cargaron más autos, fin del scroll.")
                break
            autos_previos = cantidad_actual

        # Procesar todas las tarjetas encontradas
        for tarjeta in tarjetas:
            try:
                # URL
                try:
                    enlace = tarjeta.find_element(By.CSS_SELECTOR, "a.text-blue")
                    url_auto = enlace.get_attribute("href")
                except:
                    url_auto = "No especificado"

                if url_auto in urls_vistas:
                    continue
                urls_vistas.add(url_auto)

                # Marca y modelo
                try:
                    marca = enlace.text.strip().split("\n")[0]
                    modelo = enlace.find_element(By.CSS_SELECTOR, "span.font-weight-light").text.strip()
                except:
                    marca = "No especificado"
                    modelo = "No especificado"

                # Precio
                try:
                    precio_txt = tarjeta.find_element(By.CSS_SELECTOR, "h3.card-title.openS").text.strip()
                    precio = limpiar_numero(precio_txt)
                except:
                    precio = 0

                # Detalles (año, transmisión, combustible, km)
                try:
                    detalles = tarjeta.find_elements(By.CSS_SELECTOR, "span.minificha-detail.text-blue.pt-2")
                    year = limpiar_numero(detalles[0].text) if len(detalles) > 0 else 0
                    transmision = detalles[1].text.strip() if len(detalles) > 1 else "No especificado"
                    combustible = detalles[2].text.strip() if len(detalles) > 2 else "No especificado"
                    kilometraje = limpiar_numero(detalles[3].text) if len(detalles) > 3 else 0
                except:
                    year = 0
                    transmision = "No especificado"
                    combustible = "No especificado"
                    kilometraje = 0

                ciudad = "No especificado"

                auto = {
                    "marca": marca,
                    "modelo": modelo,
                    "year": year,
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

            except Exception:
                continue

        print(f"✅ Extracción terminada: {len(lista_autos)} vehículos únicos en Piamonte Usados.")
        return lista_autos

    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
        return lista_autos

    finally:
        driver.quit()




