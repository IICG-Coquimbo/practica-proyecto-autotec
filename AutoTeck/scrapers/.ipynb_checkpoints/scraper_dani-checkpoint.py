def ejecutar_extraccion():

    # --- PASO 0: LIMPIEZA TOTAL Y REPARACIÓN ---
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

    # --- VARIABLES GENERALES ---
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "daniela"
    lista_autos = []
    driver = None

    # --- PASO 1: CONFIGURACIÓN DEL NAVEGADOR ---
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--headless=new")

    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Navegador iniciado correctamente.")

        limite_paginas = 5

        for nivel_pagina in range(limite_paginas):
            if nivel_pagina == 0:
                url_pagina = "https://www.yapo.cl/autos-usados"
            else:
                url_pagina = f"https://www.yapo.cl/autos-usados.{nivel_pagina + 1}"

            driver.get(url_pagina)
            print(f"--- Procesando Página {nivel_pagina + 1} ---")
            print(f"URL actual: {url_pagina}")

            time.sleep(10)

            WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.d3-ad-tile__description")
                )
            )

            bloques = driver.find_elements(
                By.CSS_SELECTOR, "a.d3-ad-tile__description"
            )

            print(f"Autos encontrados en página {nivel_pagina + 1}: {len(bloques)}")

            for bloque in bloques:
                try:
                    nombre = bloque.find_element(
                        By.CSS_SELECTOR, "span.d3-ad-tile__title"
                    ).text

                    try:
                        precio = bloque.find_element(
                            By.CSS_SELECTOR, "div.d3-ad-tile__price"
                        ).text
                    except:
                        precio = "0"

                    try:
                        ubicacion = bloque.find_element(
                            By.CSS_SELECTOR, "div.d3-ad-tile__location"
                        ).text
                    except:
                        ubicacion = ""

                    link = bloque.get_attribute("href")

                    lista_autos.append({
                        "identificador": nombre,
                        "valor": precio,
                        "ubicacion": ubicacion,
                        "url": link,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    })
                except:
                    continue

        print(f"✅ Extracción terminada: {len(lista_autos)} autos.")

    except Exception as e:
        print(f"❌ Error en Selenium: {e}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except:
                pass

    # 🔥 MONGO (lo dejamos igual como pediste)
    try:
        client = MongoClient("mongodb", 27017, serverSelectionTimeoutMS=5000)
        db = client["proyecto_bigdata"]
        coleccion = db["YapoAutos"]

        if lista_autos:
            for d in lista_autos:
                v_limpio = (
                    str(d["valor"])
                    .replace("$", "")
                    .replace(".", "")
                    .replace(",", "")
                    .strip()
                )
                d["valor"] = float(v_limpio) if v_limpio.isdigit() else 0.0

            coleccion.insert_many(lista_autos)
            print("✅ Datos cargados en MongoDB correctamente.")
        else:
            print("⚠️ No hay datos para guardar.")

    except Exception as e:
        print(f"❌ Error en MongoDB: {e}")

    # 🔥 ESTO ES CLAVE
    return lista_autos