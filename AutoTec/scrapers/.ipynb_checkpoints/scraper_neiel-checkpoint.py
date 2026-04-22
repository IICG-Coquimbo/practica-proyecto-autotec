import os
import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cierra procesos viejos que hayan quedado abiertos
os.system("pkill -9 chrome")
os.system("pkill -9 chromedriver")
os.system("rm -rf /tmp/.com.google.Chrome.*")
os.system("rm -rf /tmp/.org.chromium.Chromium.*")
print("🧹 Limpieza de procesos y temporales completada.")

def ejecutar_extraccion():
    # --- VARIABLES GENERALES ---
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Neiel"
    lista_autos = []   # Se define fuera del try para que siempre exista
    driver = None        # Se define fuera del try para poder cerrarlo con seguridad
    
    # --- PASO 1: CONFIGURACIÓN DEL NAVEGADOR ---
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"  # Ruta del binario de Chrome
    
    # Argumentos de estabilidad para Docker
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    
    # User-Agent común
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    
    try:
        # Inicia el navegador
        driver = webdriver.Chrome(options=options)
        print(" Navegador iniciado correctamente.")
    
        # --- PASO 2: NAVEGACIÓN Y EXTRACCIÓN ---
        limite_paginas = 3
        driver.get("https://www.autocosmos.cl/auto/usado")
    
        for nivel_pagina in range(limite_paginas):
            print(f"--- Procesando Página {nivel_pagina + 1} ---")
    
            # Espera fija para que la página termine de cargar
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Espera a que el scroll cargue todo
    
            # Espera explícita a que existan resultados
            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "article.listing-card")
                )
            )
    
            bloques = driver.find_elements(
                By.CSS_SELECTOR, "article.listing-card"
            )
    
            for bloque in bloques:
                try:
                    enlace = bloque.find_element(By.CSS_SELECTOR, "a")
                    nombre = enlace.get_attribute("title")
                    if not nombre:
                        nombre = enlace.text
                        
                    try:
                        precio_elemento = bloque.find_element(By.CSS_SELECTOR, "span[class*='price-value']")
                        # Intentamos sacar el valor del meta tag como antes, 
                        # y si no, el texto plano.
                        precio_limpio = precio_elemento.find_element(By.TAG_NAME, "meta").get_attribute("content")
                    except:
                        # Si falla el meta, sacamos el texto (ej: $7.590.000)
                        precio_limpio = precio_elemento.text
    
                    
                    lista_autos.append({
                       "identificador": nombre.strip(),
                        "valor": precio_limpio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    })
                except Exception as e:
                    
                    continue
    
            # Intenta avanzar a la siguiente página
            try:
                # Hacemos scroll hasta el final de la página para que el botón sea visible
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # En Autocosmos suele ser un <a> con clase 'next' o que contiene el icono >
                btn_sig = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.pagination__next, a[rel='next']"))
                )      
                # Usar JavaScript para hacer click es más seguro en Docker/VNC
                driver.execute_script("arguments[0].click();", btn_sig)
                print(f"👉 Avanzando a la página {nivel_pagina + 2}...")
                time.sleep(5) # Espera a que cargue la nueva página
                
            except Exception as e:
                print(f"No se pudo avanzar más: ya es la última página o el botón cambió.")
                break
    
        print(f" Extracción terminada: {len(lista_autos)} productos.")
    
    except Exception as e:
        print(f" Error en Selenium: {e}")
    
    finally:
        # Cierra el navegador solo si logró abrirse
        if driver is not None:
            try:
                driver.quit()
            except:
                pass
    
    # --- PASO 3: GUARDAR EN MONGODB (CORREGIDO) ---
    try:
        client = MongoClient("mongodb", 27017, serverSelectionTimeoutMS=5000)
        db = client["proyecto_bigdata"]
        coleccion = db["prueba_semana7"]
    
        if lista_autos:
            for d in lista_autos:
                # 1. Convertimos a string y quitamos todo lo que no sea número
                # Quitamos: puntos, comas, el signo $ y espacios
                v_sucio = str(d["valor"])
                v_limpio = v_sucio.replace(".", "").replace(",", "").replace("$", "").strip()
                
                # 2. Intentamos la conversión de forma segura
                try:
                    # Si después de limpiar quedó algo, lo convertimos
                    if v_limpio:
                        d["valor"] = float(v_limpio)
                    else:
                        d["valor"] = 0.0
                except ValueError:
                    # Si por alguna razón falla (ej: el precio decía "Consultar")
                    d["valor"] = 0.0
    
            #coleccion.insert_many(lista_autos)
            print(f"✅ {len(lista_autos)} datos cargados en MongoDB con precios corregidos.")
        else:
            print(" No hay datos para guardar.")
    
    except Exception as e:
        print(f" Error en MongoDB: {e}")

    return lista_autos
if __name__ == "__main__":
    resultados = ejecutar_extraccion()
    print(resultados[:5])
    print("Total extraídos:", len(resultados))