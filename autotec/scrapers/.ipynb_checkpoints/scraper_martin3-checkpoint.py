import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NOMBRE_GRUPO = "AutoTec"
USUARIO = "Martin"

def limpiar_numero(texto):
    if not texto:
        return 0
    # Limpia puntos, símbolos de peso y espacios
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0

def ejecutar_extraccion():
    # Limpieza de procesos previos
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")

    URL_BASE = "https://www.piamonteusados.cl/autos/seminuevos?annio_desde=&annio_hasta=&precios=&unidades=30"
    lista_autos = []
    urls_vistas = set()

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-allow-origins=*")

    # USAR EL BINARIO DEL SISTEMA (Más estable en Docker)
    driver = webdriver.Chrome(options=options)
    
    print(f"🌐 [{USUARIO}] Iniciando extracción en Piamonte Usados...")

    try:
        driver.get(URL_BASE)

        # Espera explícita para que carguen las tarjetas
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.card-index"))
            )
        except:
            print("⚠️ Timeout: No se detectaron tarjetas. La página tardó mucho en cargar.")
            return []

        # Realizamos 3 scrolls para cargar más contenido (ajustable)
        for i in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(4)
            print(f"📄 Scroll {i+1} completado...")

        tarjetas = driver.find_elements(By.CSS_SELECTOR, "div.card-index")
        
        for tarjeta in tarjetas:
            try:
                # Extraer link
                enlace = tarjeta.find_element(By.CSS_SELECTOR, "a")
                url_auto = enlace.get_attribute("href")

                if not url_auto or url_auto in urls_vistas:
                    continue
                urls_vistas.add(url_auto)

                # Datos básicos
                texto_tarjeta = tarjeta.text
                lineas = texto_tarjeta.split('\n')
                
                # Piamonte suele tener Marca y Modelo en las primeras líneas
                marca_modelo = lineas[0].strip()
                precio_txt = next((l for l in lineas if "$" in l), "0")
                
                # Detalles específicos (Año, KM, etc)
                detalles = tarjeta.find_elements(By.CSS_SELECTOR, "span.minificha-detail")
                
                auto = {
                    "marca": marca_modelo.split()[0] if marca_modelo else "Desconocido",
                    "modelo": " ".join(marca_modelo.split()[1:]) if marca_modelo else "Desconocido",
                    "year": limpiar_numero(detalles[0].text) if len(detalles) > 0 else 0,
                    "kilometraje": limpiar_numero(detalles[3].text) if len(detalles) > 3 else 0,
                    "combustible": detalles[2].text.strip() if len(detalles) > 2 else "No especificado",
                    "ciudad": "santiago", # Piamonte es principalmente RM
                    "url": url_auto,
                    "precio": limpiar_numero(precio_txt),
                    "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "grupo": NOMBRE_GRUPO,
                    "usuario": USUARIO
                }

                if auto["precio"] > 0:
                    lista_autos.append(auto)

            except Exception:
                continue

        print(f"✅ [{USUARIO}] Terminó: {len(lista_autos)} vehículos encontrados.")
        return lista_autos

    except Exception as e:
        print(f"❌ Error en el proceso de {USUARIO}: {e}")
        return []

    finally:
        driver.quit()