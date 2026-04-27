def ejecutar_extraccion():

    import os
    import time
    import re
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # --- LIMPIEZA ---
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")
    os.system("rm -rf /tmp/.com.google.Chrome.*")
    os.system("rm -rf /tmp/.org.chromium.Chromium.*")

    print("🧹 limpieza realizada")

    lista_autos = []
    driver = None

    NOMBRE_GRUPO = "autotec"
    USUARIO = "dani"

    # --- NAVEGADOR ---
    options = Options()
    options.binary_location = "/usr/bin/google-chrome"
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless=new")

    try:
        driver = webdriver.Chrome(options=options)
        print("✅ navegador iniciado")

        for pagina in range(5):

            url = "https://www.yapo.cl/autos-usados" if pagina == 0 else f"https://www.yapo.cl/autos-usados.{pagina + 1}"
            driver.get(url)

            print(f"📄 procesando página {pagina + 1}")
            time.sleep(8)

            bloques = WebDriverWait(driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, "a.d3-ad-tile__description")
                )
            )

            for bloque in bloques:
                try:
                    nombre = bloque.find_element(
                        By.CSS_SELECTOR, "span.d3-ad-tile__title"
                    ).text.lower().strip()

                    partes = nombre.split()
                    marca = partes[0] if len(partes) > 0 else ""
                    modelo = " ".join(partes[1:]) if len(partes) > 1 else ""

                    # --- precio ---
                    try:
                        precio_elemento = bloque.find_element(
                            By.CSS_SELECTOR, "div.d3-ad-tile__price"
                        )

                        precio_texto = driver.execute_script(
                            "return arguments[0].childNodes[0].textContent;",
                            precio_elemento
                        ).strip()

                    except:
                        precio_texto = ""

                    numeros = re.findall(r"\d+", precio_texto)
                    precio = int("".join(numeros)) if numeros else None

                    # --- ciudad ---
                    try:
                        ciudad = bloque.find_element(
                            By.CSS_SELECTOR, "div.d3-ad-tile__location"
                        ).text.lower().strip()
                    except:
                        ciudad = ""

                    # --- url ---
                    url_auto = bloque.get_attribute("href")

                    # --- detalles ---
                    detalles = bloque.find_elements(
                        By.CSS_SELECTOR, "li.d3-ad-tile__details-item"
                    )

                    año = ""
                    kilometraje = ""
                    combustible = ""

                    for d in detalles:
                        texto = d.text.lower().strip()

                        if texto.isdigit() and len(texto) == 4:
                            año = texto
                        elif "km" in texto:
                            kilometraje = texto
                        elif texto in [
                            "bencina", "diesel", "diésel",
                            "hibrido", "híbrido",
                            "electrico", "eléctrico"
                        ]:
                            combustible = texto

                    lista_autos.append({
                        "marca": marca,
                        "modelo": modelo,
                        "año": año,
                        "kilometraje": kilometraje,
                        "combustible": combustible,
                        "ciudad": ciudad,
                        "url": url_auto,
                        "precio": precio,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "usuario": USUARIO
                    })

                except Exception as e:
                    print("⚠️ error:", e)
                    continue

        print(f"✅ autos extraidos: {len(lista_autos)}")

    except Exception as e:
        print("❌ error selenium:", e)

    finally:
        if driver:
            driver.quit()

    return lista_autos