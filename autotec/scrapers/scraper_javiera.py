import sys
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def iniciar_driver():
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    return driver, wait


def extraer_marca_modelo(link):
    try:
        partes_url = link.split("/marcas/")[1].split("/")
        marca = partes_url[0].replace("-", " ").title()
        slug = partes_url[2]
        slug = re.sub(r"-\d+$", "", slug)
        slug = slug.replace(partes_url[0] + "-", "")
        modelo = slug.replace("-", " ").title()
        return marca, modelo
    except Exception:
        return None, None


def reiniciar_driver(driver):
    try:
        driver.quit()
    except Exception:
        pass
    return iniciar_driver()


def ejecutar_extraccion(max_paginas=50, reiniciar_cada=100):
    driver, wait = iniciar_driver()
    NOMBRE = "Javiera Pizarro"
    FECHA = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    datos_base = []
    datos_finales = []
    urls_vistas = set()

    try:
        print("Iniciando extracción...")

        for pagina in range(1, max_paginas + 1):
            url = f"https://www.clicar.cl/vehiculos/usado?page={pagina}"
            print(f"[PÁGINA {pagina}/{max_paginas}] {url}")

            try:
                driver.get(url)
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.h-fit")))
                autos = driver.find_elements(By.CSS_SELECTOR, "li.h-fit")
                print(f"  Autos encontrados: {len(autos)}")
            except Exception as e:
                print(f"  Error cargando página {pagina}: {e}")
                continue

            for auto in autos:
                try:
                    texto = auto.text.strip()
                    if not texto:
                        continue

                    link = auto.find_element(By.TAG_NAME, "a").get_attribute("href")
                    if not link or link in urls_vistas:
                        continue

                    urls_vistas.add(link)
                    lineas = [x.strip() for x in texto.split("\n") if x.strip()]
                    marca, modelo = extraer_marca_modelo(link)
                    texto_completo = " ".join(lineas)

                    match_year = re.search(r"\b(20\d{2})\b", texto_completo)
                    year = match_year.group(1) if match_year else None

                    match_km = re.search(r"(\d{1,3}(?:\.\d{3})*)\s*Km", texto_completo, re.IGNORECASE)
                    kilometraje = match_km.group(1) + " Km" if match_km else None

                    precio = None
                    for i, linea in enumerate(lineas):
                        if linea == "$" and i + 1 < len(lineas):
                            precio = "$" + lineas[i + 1]
                            break

                    datos_base.append({
                        "marca": marca,
                        "modelo": modelo,
                        "year": year,
                        "kilometraje": kilometraje,
                        "combustible": "No especificado",
                        "ciudad": "No disponible",
                        "url": link,
                        "precio": precio,
                        "nombre": NOMBRE,
                        "fecha_captura": FECHA
                    })
                except Exception as e:
                    print(f"  Error leyendo auto en página {pagina}: {e}")
                    continue

        print(f"\nTotal links base: {len(datos_base)}")
        print("Iniciando detalle por vehículo...")

        for i, dato in enumerate(datos_base, start=1):
            if reiniciar_cada and i > 1 and (i - 1) % reiniciar_cada == 0:
                print(f"\nReiniciando driver en detalle {i}...")
                driver, wait = reiniciar_driver(driver)

            try:
                print(f"[DETALLE {i}/{len(datos_base)}] {dato['url']}")
                driver.get(dato["url"])
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
                texto_original = driver.find_element(By.TAG_NAME, "body").text
                texto = texto_original.lower()

                ciudad = "No disponible"
                for linea in texto_original.split("\n"):
                    if "," in linea and "vehículo" not in linea.lower():
                        posible_ciudad = linea.split(",")[-1].strip()
                        if 2 < len(posible_ciudad) < 40:
                            ciudad = posible_ciudad
                            break

                if "gasolina" in texto:
                    combustible = "Gasolina"
                elif "diesel" in texto or "diésel" in texto:
                    combustible = "Diesel"
                elif "híbrido" in texto or "hibrido" in texto:
                    combustible = "Híbrido"
                elif "eléctrico" in texto or "electrico" in texto:
                    combustible = "Eléctrico"
                elif "petróleo" in texto or "petroleo" in texto:
                    combustible = "Petróleo"
                else:
                    combustible = "No especificado"

                dato["ciudad"] = ciudad
                dato["combustible"] = combustible
                datos_finales.append(dato)

            except Exception as e:
                print(f"  Error en detalle {i}: {e}")
                datos_finales.append(dato)
                try:
                    driver, wait = reiniciar_driver(driver)
                except Exception as e2:
                    print(f"  No se pudo reiniciar driver: {e2}")

    finally:
        try:
            driver.quit()
        except Exception:
            pass

    print("\n🔥 LISTO")
    print("📦 Total:", len(datos_finales))
    return datos_finales


if __name__ == "__main__":
    max_paginas = 50
    if len(sys.argv) > 1:
        max_paginas = int(sys.argv[1])

    resultados = ejecutar_extraccion(max_paginas=max_paginas, reiniciar_cada=100)
    print(f"Total extraído final: {len(resultados)}")
