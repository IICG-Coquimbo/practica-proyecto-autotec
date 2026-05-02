#valentini
import os
import time
from selenium import webdriver # Faltaba
from selenium.webdriver.chrome.options import Options # Faltaba
from selenium.webdriver.common.by import By

# =========================
# LIMPIEZA
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

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")
    # User-agent para evitar detecciones de bot
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        print("Navegador iniciado correctamente para Valentini.")

        limite_paginas = 3 # Ajustado para pruebas
        URL_BASE = "https://seminuevosvalentini.cl/search/page/{}/"

        for pagina in range(1, limite_paginas + 1):
            url = URL_BASE.format(pagina)
            print(f"Buscando en: {url}")
            
            try:
                driver.get(url)
                time.sleep(5)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

                # BLOQUES DE AUTOS
                bloques = driver.find_elements(By.CSS_SELECTOR, "div.vehica-car-card__content")

                for bloque in bloques:
                    try:
                        # NOMBRE + URL
                        nombre_elemento = bloque.find_element(By.CSS_SELECTOR, "a.vehica-car-card__name")
                        nombre = nombre_elemento.text.strip()
                        url_auto = nombre_elemento.get_attribute("href")

                        # PRECIO
                        try:
                            precio = bloque.find_element(By.CSS_SELECTOR, "div.vehica-car-card__price").text.strip()
                        except:
                            precio = "0"

                        # INFORMACION EXTRA
                        infos = bloque.find_elements(By.CSS_SELECTOR, "div.vehica-car-card_info_single")
                        
                        year = infos[0].text if len(infos) > 0 else "0"
                        kilometraje = infos[1].text if len(infos) > 1 else "0"
                        combustible = infos[3].text if len(infos) > 3 else "N/A"

                        # SEPARAR MARCA Y MODELO
                        partes_nombre = nombre.split(" ", 1)
                        marca = partes_nombre[0] if len(partes_nombre) > 0 else "N/A"
                        modelo = partes_nombre[1] if len(partes_nombre) > 1 else "N/A"

                        lista_autos.append({
                            "marca": marca,
                            "modelo": modelo,
                            "year": year,
                            "kilometraje": kilometraje,
                            "combustible": combustible,
                            "ciudad": "N/A",
                            "url": url_auto,
                            "precio": precio,
                            "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                            "grupo": NOMBRE_GRUPO,
                            "usuario": USUARIO
                        })
                    except:
                        continue
                
                print(f"   Página {pagina} lista. Acumulado: {len(lista_autos)}")

            except Exception as e:
                print(f"Error en página {pagina}: {e}")
                continue

        return lista_autos

    except Exception as e:
        print(f"Error Selenium Valentini: {e}")
        return []

    finally:
        if driver is not None:
            print("Cerrando navegador Valentini...")
            driver.quit()