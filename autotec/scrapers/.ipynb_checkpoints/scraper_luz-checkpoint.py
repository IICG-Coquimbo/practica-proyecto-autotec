import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ================= FUNCIONES DE APOYO =================

def limpiar_numero(texto):
    return int(re.sub(r"[^\d]", "", texto)) if texto else 0

def separar_marca_modelo(titulo):
    partes = titulo.split()
    marca = partes[0] if len(partes) > 0 else "N/A"
    modelo = " ".join(partes[1:]) if len(partes) > 1 else "N/A"
    return marca, modelo

def extraer_info(info):
    # Emol separa por "|" (Ej: "2022 | 45.000 km | Bencina | Santiago")
    partes = [p.strip() for p in info.split("|")]
    
    year = "0"
    if len(partes) > 0:
        match_year = re.search(r"\d{4}", partes[0])
        year = match_year.group() if match_year else "0"

    km = limpiar_numero(partes[1]) if len(partes) > 1 else 0
    combustible = partes[2] if len(partes) > 2 else "No disponible"
    ciudad = partes[3] if len(partes) > 3 else "No disponible"

    return year, km, combustible, ciudad

# ================= FUNCIÓN PRINCIPAL =================

def ejecutar_extraccion(meta=500):
    NOMBRE = "Luz Azocar"
    GRUPO = "AutoTec"
    URL_BASE = "https://automoviles.emol.com/venta/autos-usados"
    
    # Configuración de Selenium
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(options=options)
    
    total = 0
    pagina = 1
    links_vistos = set()
    datos_finales = []

    print(f"🚀 Iniciando Emol para {meta} registros...")

    try:
        while total < meta:
            url = f"{URL_BASE}?p={pagina}"
            driver.get(url)
            time.sleep(2) # Emol es rápido, no necesita esperas tan largas

            # Selector específico de Emol para cada auto
            autos = driver.find_elements(By.CSS_SELECTOR, "article.search-result.row")

            if not autos:
                print(f"  🏁 Fin de resultados en página {pagina}")
                break

            for auto in autos:
                if total >= meta:
                    break

                try:
                    # Extracción directa desde la lista
                    precio_texto = auto.find_element(By.TAG_NAME, "h4").text
                    precio = limpiar_numero(precio_texto)
                    
                    titulo = auto.find_element(By.TAG_NAME, "h3").text
                    info = auto.find_element(By.TAG_NAME, "p").text
                    link = auto.find_element(By.CSS_SELECTOR, "a.ga").get_attribute("href")

                    if link in links_vistos or precio == 0:
                        continue

                    marca, modelo = separar_marca_modelo(titulo)
                    year, km, combustible, ciudad = extraer_info(info)
                    
                    try:
                        img = bloque.find_element(By.CSS_SELECTOR, "div.thumbnail img.lazy")
                        foto_url = (
                            img.get_attribute("data-original")
                            or img.get_attribute("src")
                            or ""
                        ).strip()
                    except Exception:
                        foto_url = ""
                        
                    registro = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": km,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": link,
                        "precio": precio,
                        "foto_url": foto_url,
                        "usuario": NOMBRE,
                        "fecha_captura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": GRUPO,
                    }

                    datos_finales.append(registro)
                    links_vistos.add(link)
                    total += 1

                except Exception:
                    continue
            
            pagina += 1

    finally:
        driver.quit()
        print("🔒 Navegador de Luz cerrado.")

    return datos_finales