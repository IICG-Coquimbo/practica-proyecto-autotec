import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# --- Variables globales ---
NOMBRE_GRUPO = "AutoTec"
USUARIO = "Martin"

# --- Funciones auxiliares ---
def limpiar_numero(texto):
    if not texto:
        return 0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return int(limpio) if limpio else 0

# --- Función principal de extracción ---
def ejecutar_extraccion(meta_autos=500):
    URL_BASE = "https://www.difor.cl/autos-usados-chile?page="
    lista_autos = []

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    # Usamos el driver estándar del entorno
    driver = webdriver.Chrome(options=options)
    
    print(f"🚀 Iniciando Difor para {meta_autos} autos...")

    try:
        pagina = 1
        # Difor suele tener entre 30 y 40 páginas
        while len(lista_autos) < meta_autos:
            url_pagina = f"{URL_BASE}{pagina}"
            driver.get(url_pagina)
            time.sleep(3)

            # Buscamos las tarjetas de productos
            tarjetas = driver.find_elements(By.XPATH, "//a[@id='product-card-link']")

            if not tarjetas:
                print(f"  🏁 No hay más resultados en la página {pagina}.")
                break

            for tarjeta in tarjetas:
                if len(lista_autos) >= meta_autos:
                    break

                try:
                    href = tarjeta.get_attribute("href")
                    url_auto = "https://www.difor.cl" + href if href.startswith("/") else href

                    # Marca, modelo y año desde el título
                    try:
                        titulo = tarjeta.find_element(By.XPATH, ".//p[contains(@class,'MuiTypography-body1')]").text.strip()
                        partes = titulo.split()
                        marca = partes[0] if len(partes) > 0 else "N/A"
                        # El año suele ser la última palabra
                        year = partes[-1] if partes[-1].isdigit() else "0"
                        modelo = " ".join(partes[1:-1]) if len(partes) > 2 else "N/A"
                    except:
                        marca = modelo = "N/A"
                        year = "0"

                    # Precio
                    try:
                        precio_txt = tarjeta.find_element(By.XPATH, ".//p[contains(@class,'MuiTypography-body2')]").text.strip()
                        precio = limpiar_numero(precio_txt)
                    except:
                        precio = 0

                    # Kilometraje y Combustible (están en spans dentro de la tarjeta)
                    kilometraje = 0
                    combustible = "N/A"
                    try:
                        spans = tarjeta.find_elements(By.XPATH, ".//span")
                        for sp in spans:
                            txt = sp.text.strip().upper()
                            if "KM" in txt:
                                kilometraje = limpiar_numero(txt)
                            elif any(c in txt for c in ["DIESEL", "BENCINA", "GASOLINA", "HIBRIDO", "ELECTRICO"]):
                                combustible = txt.capitalize()
                    except:
                        pass

                    try:
                        img = bloque.find_element(By.CSS_SELECTOR, "div#grid-product-card-img img")
                        foto_url = img.get_attribute("src") or ""
                    except Exception:
                        foto_url = ""

                    auto = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": kilometraje,
                        "combustible": combustible,
                        "ciudad": "Chile (Sucursal Difor)",
                        "url": url_auto,
                        "precio": precio,
                        "foto_url": foto_url,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO,
                    }

                    lista_autos.append(auto)

                except Exception:
                    continue
            
            pagina += 1

    except Exception as e:
        print(f"❌ Error en Difor: {e}")
    
    finally:
        driver.quit()
        print("🔒 Navegador de Martin cerrado.")

    return lista_autos