#salazarisrael
import time
import re
from pymongo import MongoClient
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

print("🧹 Limpieza de procesos y temporales completada.")


def ejecutar_extraccion():
    NOMBRE_GRUPO = "AutoTec"
    USUARIO = "Belen A"
    lista_autos = []
    autos_vistos = set()

    options = uc.ChromeOptions()

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(
        options=options,
        version_main=147,
        use_subprocess=True
    )

    print("Navegador iniciado correctamente.")

    URL_BASE = "https://www.salazarisrael.cl/vehiculos/usado?page={}"

    MAX_PAGINAS = 60

    # SCRAPING

    for pagina in range(1, MAX_PAGINAS + 1):

        try:

            driver.get(URL_BASE.format(pagina))

            time.sleep(5)

            autos = driver.find_elements(By.CSS_SELECTOR, "article")

            if len(autos) == 0:
                break

            for auto in autos:

                try:

                    texto = auto.text.strip()

                    if len(texto) < 20:
                        continue


                    try:
                        link = auto.find_element(By.TAG_NAME, "a")
                        url_auto = link.get_attribute("href")
                    except:
                        url_auto = "N/A"

                    if url_auto in autos_vistos:
                        continue

                    autos_vistos.add(url_auto)


                    lineas = [
                        l.strip()
                        for l in texto.split("\n")
                        if l.strip()
                    ]


                    detalle = ""

                    for l in lineas:

                        if "|" in l and "Km" in l:
                            detalle = l
                            break

                    if detalle == "":
                        continue


                    lineas_utiles = []

                    for l in lineas:

                        if (
                            "$" not in l
                            and "Cuota" not in l
                            and "RESERVAR" not in l
                            and "COTIZAR" not in l
                            and "VER MÁS" not in l
                            and "Cotiza ahora" not in l
                            and "Incluye bono" not in l
                            and "|" not in l
                            and "Km" not in l
                            and len(l.strip()) > 1
                        ):
                            lineas_utiles.append(l)


                    marca = "N/A"
                    modelo = "N/A"

                    lineas_finales = []

                    for l in lineas_utiles:

                        texto_limpio = l.lower().strip()

                    # ====================================
                    # IGNORAR TIPOS VEHICULO
                    # ====================================

                        if texto_limpio in [
                            "camioneta",
                            "suv",
                            "station wagon",
                            "sedan",
                            "hatchback",
                            "coupe",
                            "convertible",
                            "van",
                            "automovil"
                        ]:
                            continue

                    # ====================================
                    # IGNORAR BADGES / ETIQUETAS
                    # ====================================

                        palavras_bloqueadas = [
                            "bajo",
                            "kilometraje",
                            "mantención",
                            "mantencion",
                            "taller",
                            "poco kilometraje",
                            "un dueño",
                            "único dueño",
                            "garantía",
                            "garantia"
                        ]

                        if any(p in texto_limpio for p in palavras_bloqueadas):
                            continue


                        if len(l.split()) > 6:
                            continue


                        if re.search(r'^\d[\d\.]+$', l):
                            continue

                        lineas_finales.append(l)


                    if len(lineas_finales) >= 3:

                        marca = lineas_finales[0]

                        modelo_base = lineas_finales[1]

                        detalle_modelo = lineas_finales[2]

                        modelo = f"{modelo_base} {detalle_modelo}"

                    elif len(lineas_finales) == 2:

                        marca = lineas_finales[0]

                        modelo = lineas_finales[1]

                    elif len(lineas_finales) == 1:

                        marca = lineas_finales[0]

                        modelo = "N/A"

                    print("MARCA:", marca)
                    print("MODELO:", modelo)


                    year = "N/A"

                    year_match = re.search(
                        r'\b(19|20)\d{2}\b',
                        detalle
                    )

                    if year_match:
                        year = year_match.group()


                    kilometraje = "N/A"

                    km_match = re.search(
                        r'([\d\.]+)\s*Km',
                        detalle
                    )

                    if km_match:
                        kilometraje = km_match.group(1)


                    combustible = "N/A"
    
                    partes = [p.strip() for p in detalle.split("|")]

                    if len(partes) >= 4:
                        combustible = partes[3]



                    precio = "0"

                    for i, l in enumerate(lineas):

                        if l == "$":

                            if i + 1 < len(lineas):

                                posible_precio = lineas[i + 1]

                                if re.search(r'[\d\.]+', posible_precio):

                                    precio = "$" + posible_precio
                                    break


                    if marca == "N/A":
                        continue


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


                except Exception as e:
                    print("Error auto:", e)

            print(f"TOTAL ACUMULADO: {len(lista_autos)}")
            return lista_autos

        except Exception as e:
            print(f"ERROR PAGINA {pagina}: {e}")

    driver.quit()

    print(f"\nTOTAL FINAL: {len(lista_autos)} autos")