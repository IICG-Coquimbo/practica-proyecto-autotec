import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# ================= CONFIG =================

NOMBRE = "Luz Azocar"
GRUPO = "AutoTec"
FECHA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

META = 500
URL_BASE = "https://automoviles.emol.com/venta/autos-usados"

# ================= FUNCIONES =================

def limpiar_numero(texto):
    return int(re.sub(r"[^\d]", "", texto)) if texto else 0

def separar_marca_modelo(titulo):
    partes = titulo.split()
    marca = partes[0] if len(partes) > 0 else None
    modelo = " ".join(partes[1:]) if len(partes) > 1 else None
    return marca, modelo

def extraer_info(info):
    partes = [p.strip() for p in info.split("|")]

    year = None
    if len(partes) > 0:
        match_year = re.search(r"\d{4}", partes[0])
        if match_year:
            year = int(match_year.group())

    km = limpiar_numero(partes[1]) if len(partes) > 1 else 0
    combustible = partes[2] if len(partes) > 2 else "No disponible"
    ciudad = partes[3] if len(partes) > 3 else "No disponible"

    return year, km, combustible, ciudad

# ================= FUNCIÓN PRINCIPAL =================

def ejecutar_extraccion():

    total = 0
    pagina = 1
    links_vistos = set()
    datos_finales = []

    # ================= SELENIUM =================
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    print("Iniciando scraping...")

    try:
        while total < META:

            url = f"{URL_BASE}?p={pagina}"
            driver.get(url)
            time.sleep(3)

            autos = driver.find_elements(By.CSS_SELECTOR, "article.search-result.row")

            if len(autos) == 0:
                print(f"Página {pagina} sin resultados")
                break

            guardados_pagina = 0

            for auto in autos:

                if total >= META:
                    break

                try:
                    precio = limpiar_numero(auto.find_element(By.TAG_NAME, "h4").text)
                    titulo = auto.find_element(By.TAG_NAME, "h3").text
                    info = auto.find_element(By.TAG_NAME, "p").text
                    link = auto.find_element(By.CSS_SELECTOR, "a.ga").get_attribute("href")

                    if link in links_vistos:
                        continue

                    marca, modelo = separar_marca_modelo(titulo)
                    year, km, combustible, ciudad = extraer_info(info)

                    # VALIDACIÓN CORRECTA
                    if (
                        not marca or
                        not modelo or
                        not year or
                        km == 0 or
                        combustible == "No disponible" or
                        ciudad == "No disponible" or
                        not precio or
                        not link
                    ):
                        continue

                    dato = {
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": km,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": link,
                        "precio": precio,
                        "usuario": NOMBRE,
                        "fecha_captura": FECHA,
                        "grupo": GRUPO
                    }


                    datos_finales.append(dato)
                    links_vistos.add(link)
                    total += 1
                    guardados_pagina += 1

                except:
                    continue

            pagina += 1

    finally:
        driver.quit()
        print("Navegador cerrado.")

    return datos_finales


# ================= EJECUTAR =================

datos = ejecutar_extraccion()

print("Scraping finalizado")
print("Total extraído:", len(datos))