import os
import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


<<<<<<< HEAD
# ========================
# FUNCIONES AUXILIARES
# =========================
def limpiar_numero(texto):
    if not texto:
        return 0
    num = re.sub(r"[^\d]", "", texto)
    return int(num) if num else 0
=======
# =========================
# FUNCIONES DE LIMPIEZA
# =========================
def limpiar_numero(texto):
    if not texto:
        return None
    num = re.sub(r"[^\d]", "", texto)
    return int(num) if num else None
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25


def extraer_year(texto):
    match = re.search(r"\b(19[8-9][0-9]|20[0-2][0-9])\b", texto)
<<<<<<< HEAD
    return int(match.group()) if match else 0
=======
    return int(match.group()) if match else None
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25


def normalizar_combustible(texto):
    texto = texto.lower()

    if "bencina" in texto or "gasolina" in texto:
        return "gasolina"
    if "diesel" in texto or "diésel" in texto:
        return "diesel"
    if "hibrido" in texto or "híbrido" in texto:
        return "hibrido"
    if "electrico" in texto or "eléctrico" in texto:
        return "electrico"

    return "no especificado"


def separar_marca_modelo(titulo):
    partes = titulo.split()

    if len(partes) == 0:
<<<<<<< HEAD
        return "", ""
=======
        return None, None
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25

    marca = partes[0].lower()
    modelo = " ".join(partes[1:]).lower()
    modelo = re.sub(r"\b(19[8-9][0-9]|20[0-2][0-9])\b", "", modelo).strip()

    return marca, modelo


def extraer_ciudad(texto):
    ciudades = [
        "Santiago", "La Serena", "Coquimbo", "Valparaíso", "Viña del Mar",
        "Concepción", "Rancagua", "Talca", "Temuco", "Antofagasta",
        "Iquique", "Copiapó", "Chillán", "Puerto Montt", "Osorno",
        "La Florida", "Las Condes", "Maipú", "Providencia", "Ñuñoa",
        "Macul", "San Miguel", "Puente Alto", "San Bernardo", "Quilicura",
        "Huechuraba", "Recoleta", "Independencia", "Estación Central",
        "Pudahuel", "Peñalolén", "Vitacura", "Lo Barnechea"
    ]

<<<<<<< HEAD
    texto_lower = texto.lower()
    for ciudad in ciudades:
        if ciudad.lower() in texto_lower:
=======
    for ciudad in ciudades:
        if ciudad.lower() in texto.lower():
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
            return ciudad.lower()

    return "santiago"


# =========================
# DRIVER
# =========================
def iniciar_driver():
    options = Options()
    options.page_load_strategy = "eager"

    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--blink-settings=imagesEnabled=false")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    driver.set_script_timeout(30)

    return driver


# =========================
<<<<<<< HEAD
# EXTRAER BLOQUES
=======
# EXTRACCIÓN DE BLOQUES
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
# =========================
def extraer_bloques(driver, autos_extraidos, links_vistos, max_autos):
    bloques = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-item")

    for bloque in bloques:
<<<<<<< HEAD
=======

>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
        if len(autos_extraidos) >= max_autos:
            break

        try:
            texto = bloque.text.strip()

            if not texto:
                continue

            if "$" not in texto or "km" not in texto.lower():
                continue

            lineas = [linea.strip() for linea in texto.split("\n") if linea.strip()]

            titulo = None
<<<<<<< HEAD
            precio = 0
            kilometraje = 0
=======
            precio = None
            kilometraje = None
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25

            for linea in lineas:
                if re.search(r"\b(19[8-9][0-9]|20[0-2][0-9])\b", linea):
                    titulo = linea
                    break

            for linea in lineas:
                if "$" in linea:
                    precio = limpiar_numero(linea)
                    break

            for linea in lineas:
                if "km" in linea.lower():
                    kilometraje = limpiar_numero(linea)
                    break

            if not titulo:
                continue

            marca, modelo = separar_marca_modelo(titulo)
            year = extraer_year(titulo)
            combustible = normalizar_combustible(texto)
            ciudad = extraer_ciudad(texto)

            try:
<<<<<<< HEAD
                img = bloque.find_element(By.CSS_SELECTOR, "img.object-cover")
            
                foto_url = (
                    img.get_attribute("srcset")
                    or img.get_attribute("data-srcset")
                    or img.get_attribute("src")
                    or img.get_attribute("data-src")
                    or ""
                )

                if foto_url and "," in foto_url:
                    foto_url = foto_url.split(",")[-1].strip().split(" ")[0]
            
            except Exception:
                foto_url = ""

            link = ""
            selectores_link = [
                "a[href*='/autos-usados/']",
                "a[href*='/usado/']",
                "a[href*='/vehiculo/']",
                "a[href]"
            ]

            for selector in selectores_link:
                try:
                    link_elem = bloque.find_element(By.CSS_SELECTOR, selector)
                    href = link_elem.get_attribute("href")
                    if href and href.strip():
                        link = href.strip()
                        break
                except Exception:
                    pass

            if not link:
                continue
=======
                link = bloque.find_element(By.TAG_NAME, "a").get_attribute("href")
            except:
                link = None

            if not link:
                link = f"sin-url-{marca}-{modelo}-{year}-{precio}-{kilometraje}"
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25

            if link in links_vistos:
                continue

            links_vistos.add(link)

            auto = {
<<<<<<< HEAD
                "marca": marca or "",
                "modelo": modelo or "",
                "year": year or 0,
                "kilometraje": kilometraje or 0,
                "combustible": combustible or "no especificado",
                "ciudad": ciudad or "santiago",
                "url": link,
                "precio": precio or 0,
                "foto_url": foto_url or "",
                "fecha_captura": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "grupo": "autotec",
                "usuario": "jocelyn l"
            }

            autos_extraidos.append(auto)

        except Exception as e:
            print(f"Error en bloque: {e}")
=======
                "marca": marca,
                "modelo": modelo,
                "year": year,
                "kilometraje": kilometraje,
                "combustible": combustible,
                "ciudad": ciudad,
                "url": link,
                "precio": precio,
                "fecha_captura": datetime.now(),
                "grupo": "autotec",
                "usuario": "jocelyn"
            }

            if all([
                auto["marca"],
                auto["modelo"],
                auto["year"],
                auto["kilometraje"],
                auto["ciudad"],
                auto["url"],
                auto["precio"]
            ]):
                autos_extraidos.append(auto)

        except:
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
            continue


# =========================
# FUNCIÓN PRINCIPAL
# =========================
def ejecutar_extraccion(max_autos=500):
<<<<<<< HEAD
=======

>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")

    print("🔎 Iniciando scraping Bruno Fritsch...")

    driver = iniciar_driver()
<<<<<<< HEAD
=======

>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
    autos_extraidos = []
    links_vistos = set()

    url_base = "https://www.brunofritsch.cl/autos-usados"

    try:
        pagina = 1
        paginas_sin_datos = 0

        while len(autos_extraidos) < max_autos and pagina <= 45:
<<<<<<< HEAD
=======

>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
            try:
                driver.get(f"{url_base}?page={pagina}")
                time.sleep(4)

            except TimeoutException:
                try:
                    driver.execute_script("window.stop();")
                    time.sleep(2)
<<<<<<< HEAD
                except Exception:
=======
                except:
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
                    pass

            cantidad_antes = len(autos_extraidos)

            for _ in range(4):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                extraer_bloques(driver, autos_extraidos, links_vistos, max_autos)

                if len(autos_extraidos) >= max_autos:
                    break

            cantidad_despues = len(autos_extraidos)
<<<<<<< HEAD
            print(f"   Acumulado: {cantidad_despues}")
=======
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25

            if cantidad_despues == cantidad_antes:
                paginas_sin_datos += 1
            else:
                paginas_sin_datos = 0

            if paginas_sin_datos >= 5:
<<<<<<< HEAD
                print("⚠️ Se detectaron varias páginas sin datos nuevos. Fin de extracción.")
=======
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
                break

            pagina += 1

    finally:
        driver.quit()

    print("\n📊 RESULTADO FINAL")
    print(f"🚗 Autos extraídos: {len(autos_extraidos)}")

<<<<<<< HEAD
    return autos_extraidos
=======
    return autos_extraidos


# =========================
# EJECUCIÓN LOCAL
# =========================
if __name__ == "__main__":
    datos = ejecutar_extraccion(max_autos=500)
    print("Total:", len(datos))
>>>>>>> 51be041d3611d942b850bc2b7b6f833b32258a25
