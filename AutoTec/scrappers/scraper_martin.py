import os
import time
import re
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# --- LIMPIEZA ---
os.system("taskkill /F /IM chrome.exe")  # En Windows, usar taskkill para cerrar Chrome
os.system("taskkill /F /IM chromedriver.exe")  # Cerrar cualquier instancia de Chromedriver
print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Martin"  # O cualquier nombre que prefieras
    URL_OBJETIVO = "http://books.toscrape.com/"  # Cambia esta URL si es necesario
    datos_finales = []

    # --- CONFIGURACIÓN DE SELENIUM ---
    options = Options()
    options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"  # Ruta del navegador Chrome en Windows

    # Opciones para la ejecución en modo sin cabeza (headless)
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    try:
        # Inicializa el WebDriver de Selenium usando el ChromeDriver y las opciones definidas
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("🚀 Navegador iniciado correctamente.")

        # --- EJECUTAR SCRAPING ---
        driver.get(URL_OBJETIVO)

        # Esperar que la página cargue
        WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))
        )

        limite_paginas = 3  # Cambia el número de páginas que deseas scrapear

        for nivel_pagina in range(limite_paginas):
            print(f"--- Procesando Página {nivel_pagina + 1} ---")

            # Espera a que los elementos estén visibles
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "product_pod"))
            )

            bloques_primer_nivel = driver.find_elements(By.CLASS_NAME, "product_pod")

            for bloque in bloques_primer_nivel:
                try:
                    nombre = bloque.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                    precio = bloque.find_element(By.CLASS_NAME, "price_color").text

                    # Guardar los datos extraídos
                    datos_finales.append({
                        "identificador": nombre.strip(),
                        "valor": precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    })
                except Exception as e:
                    print(f"Error al procesar un bloque: {e}")

            # Intentar pasar a la siguiente página
            try:
                disparador_siguiente = driver.find_element(By.CSS_SELECTOR, "li.next a")
                disparador_siguiente.click()
                time.sleep(5)
            except:
                print("No se encontró el botón siguiente o ya es la última página.")
                break

        print(f"Extracción terminada: {len(datos_finales)} productos.")
        
    except Exception as e:
        print(f"Error en Selenium: {e}")
        
    finally:
        driver.quit()

    return datos_finales  # Retornar los datos extraídos


# --- GUARDAR EN MONGODB ---
def guardar_en_mongodb(datos):
    try:
        client = MongoClient("mongodb", 27017, serverSelectionTimeoutMS=5000)
        db = client["proyecto_bigdata"]
        coleccion = db["AutoTec"]

        if datos:
            for d in datos:
                # Limpieza del precio antes de convertirlo a número
                v_limpio = str(d["valor"]).replace(".", "").replace(",", "").replace("$", "").strip()
                d["valor"] = float(v_limpio) if v_limpio.isdigit() else 0.0

            coleccion.insert_many(datos)
            print(f"💾 {len(datos)} registros guardados en MongoDB.")
        else:
            print("⚠️ No hay datos para guardar.")
    except Exception as e:
        print(f"❌ Error en MongoDB: {e}")


# Ejecutar la extracción y guardar en MongoDB
datos_extraidos = ejecutar_extraccion()
guardar_en_mongodb(datos_extraidos)
