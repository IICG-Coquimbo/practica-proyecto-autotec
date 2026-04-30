#valentini
import os
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

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

    options = uc.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    try:

        driver = uc.Chrome(options=options, version_main=147)

        limite_paginas = 5

        URL_BASE = "https://seminuevosvalentini.cl/search/page/{}/"

        for pagina in range(1, limite_paginas + 1):

            url = URL_BASE.format(pagina)

            driver.get(url)

            time.sleep(5)

            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            time.sleep(3)

            # BLOQUES DE AUTOS
            bloques = driver.find_elements(
                By.CSS_SELECTOR,
                "div.vehica-car-card__content"
            )


            for bloque in bloques:

                try:

                    # NOMBRE + URL
                    nombre_elemento = bloque.find_element(
                        By.CSS_SELECTOR,
                        "a.vehica-car-card__name"
                    )

                    nombre = nombre_elemento.text.strip()

                    url_auto = nombre_elemento.get_attribute("href")

                    # PRECIO
                    try:
                        precio = bloque.find_element(
                            By.CSS_SELECTOR,
                            "div.vehica-car-card__price"
                        ).text.strip()
                    except:
                        precio = 0

                    # INFORMACION EXTRA
                    infos = bloque.find_elements(
                        By.CSS_SELECTOR,
                        "div.vehica-car-card__info__single"
                    )

                    year = infos[0].text if len(infos) > 0 else 0
                    kilometraje = infos[1].text if len(infos) > 1 else 0
                    combustible = infos[3].text if len(infos) > 3 else "N/A"

                    # SEPARAR MARCA Y MODELO
                    partes_nombre = nombre.split(" ", 1)

                    marca = (
                        partes_nombre[0]
                        if len(partes_nombre) > 0
                        else "N/A"
                    )

                    modelo = (
                        partes_nombre[1]
                        if len(partes_nombre) > 1
                        else "N/A"
                    )

                    # GUARDAR DATOS
                    lista_autos.append({

                        "marca": marca if marca else "N/A",

                        "modelo": modelo if modelo else "N/A",

                        "year": year if year else 0,

                        "kilometraje": kilometraje if kilometraje else 0,

                        "combustible": combustible if combustible else "N/A",

                        "ciudad": "N/A",

                        "url": url_auto if url_auto else "N/A",

                        "precio": precio if precio else 0,

                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),

                        "grupo": NOMBRE_GRUPO,

                        "usuario": USUARIO

                    })

                except Exception as e:

                    continue

            print(f"Acumulado total: {len(lista_autos)} autos")
            return lista_autos

    except Exception as e:

        print(f"Error Selenium: {e}")

    finally:

        if driver is not None:

            try:
                driver.quit()
            except:
                pass
