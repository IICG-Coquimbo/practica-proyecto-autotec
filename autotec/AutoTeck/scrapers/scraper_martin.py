import os
import time
import re
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

print("🧹 Limpieza de procesos completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Martin"
    URL_BASE = "https://seminuevos.aspillagahornauer.cl/stock-seminuevos/page/"
    datos_finales = []

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("🚀 Navegador iniciado correctamente.")

    try:
        limite_paginas = 3

        for nivel_pagina in range(1, limite_paginas + 1):
            url_pagina = f"{URL_BASE}{nivel_pagina}/"
            print(f"\n📄 Procesando Página {nivel_pagina} 👉 {url_pagina}")
            driver.get(url_pagina)
            time.sleep(5)

            # Esperar a que carguen las tarjetas de vehículos
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                    "div.listing-list-loop.stm-listing-directory-list-loop.stm-isotope-listing-item"))
            )

            tarjetas = driver.find_elements(By.CSS_SELECTOR,
                "div.listing-list-loop.stm-listing-directory-list-loop.stm-isotope-listing-item")
            print(f"🔍 Vehículos encontrados: {len(tarjetas)}")

            for tarjeta in tarjetas:
                try:
                    # Nombre y URL
                    bloque = tarjeta.find_element(By.CSS_SELECTOR, "div.title.heading-font a.rmv_txt_drctn")
                    nombre_auto = re.sub(r'\s+', ' ', bloque.text.strip())
                    url = bloque.get_attribute("href")

                    # Valores dinámicos
                    valores = tarjeta.find_elements(By.CSS_SELECTOR, "div.value")
                    marca = modelo = anio = kilometraje = combustible = transmision = ""

                    for v in valores:
                        texto = v.text.strip().upper()
                        if "KM" in texto or "KMS" in texto:
                            kilometraje = texto
                        elif texto.isdigit() and len(texto) == 4:  # año
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

                    # Ciudad
                    try:
                        ciudad_elemento = tarjeta.find_element(By.CSS_SELECTOR, "div.stm-tooltip-link")
                        ciudad = ciudad_elemento.text.strip()
                    except:
                        ciudad = ""

                    # Precio
                    precio_elementos = tarjeta.find_elements(By.CSS_SELECTOR, "span.heading-font")
                    precio = precio_elementos[0].text.strip() if precio_elementos else "Consultar"

                    precio_limpio = re.sub(r'\D', '', precio)
                    km_limpio = re.sub(r'\D', '', kilometraje)

                    datos_finales.append({
                        "marca": marca,
                        "modelo": modelo,
                        "anio": anio,
                        "kilometraje": int(km_limpio) if km_limpio else 0,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": url,
                        "precio": float(precio_limpio) if precio_limpio else 0.0,
                        "nombre": USUARIO,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO
                    })

                    print(f"✅ Capturado: {marca} {modelo} ({anio}) - {precio} en {ciudad}")

                except Exception as e:
                    print(f"⚠️ Error al procesar un vehículo: {e}")
                    continue

        print(f"\n🎉 Extracción terminada: {len(datos_finales)} vehículos capturados.")
    except Exception as e:
        print(f"❌ Error en Selenium: {e}")
    finally:
        driver.quit()

    return datos_finales


def guardar_en_mongodb(datos):
    try:
        # 🔧 Conexión corregida para Mongo local (visible en Mongo Express en http://localhost:8081)
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        db = client["proyecto_bigdata"]
        coleccion = db["AutoTec"]

        if datos:
            for d in datos:
                criterio = {
                    "marca": d["marca"],
                    "modelo": d["modelo"],
                    "anio": d["anio"],
                    "kilometraje": d["kilometraje"],
                    "ciudad": d["ciudad"]
                }
                if not coleccion.find_one(criterio):
                    coleccion.insert_one(d)
                    print(f"💾 Insertado en MongoDB: {d['marca']} {d['modelo']} ({d['anio']})")
                else:
                    print(f"⚠️ Duplicado detectado, no insertado: {d['marca']} {d['modelo']} ({d['anio']})")
        else:
            print("⚠️ No hay datos para guardar.")
    except Exception as e:
        print(f"❌ Error en MongoDB: {e}")


if __name__ == "__main__":
    datos_extraidos = ejecutar_extraccion()
    guardar_en_mongodb(datos_extraidos)

