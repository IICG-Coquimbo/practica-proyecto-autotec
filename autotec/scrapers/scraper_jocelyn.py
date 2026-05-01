import os
import re
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


# =========================
# FUNCIONES
# =========================
def limpiar_numero(texto):
    if not texto:
        return None
    num = re.sub(r"[^\d]", "", texto)
    return int(num) if num else None


def extraer_year(texto):
    match = re.search(r"\b(19[8-9][0-9]|20[0-2][0-9])\b", texto)
    return int(match.group()) if match else None


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

    return None


def separar_marca_modelo(titulo):
    partes = titulo.split()

    if len(partes) == 0:
        return None, None

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

    for ciudad in ciudades:
        if ciudad.lower() in texto.lower():
            return ciudad.lower()

    return None


# =========================
# FUNCIÓN PRINCIPAL
# =========================
def ejecutar_extraccion(max_autos=500):

    # Limpieza
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")

    print("🔎 Iniciando scraping Bruno Fritsch...")

    # Selenium
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)

    url = "https://www.brunofritsch.cl/autos-usados"
    driver.get(url)

    time.sleep(8)

    autos_extraidos = []
    links_vistos = set()

    for scroll in range(40):

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        bloques = driver.find_elements(By.CSS_SELECTOR, "div.MuiGrid-root.MuiGrid-item")

        for bloque in bloques:

            if len(autos_extraidos) >= max_autos:
                break

            try:
                texto = bloque.text.strip()

                if not texto:
                    continue

                if "$" not in texto or "km" not in texto.lower():
                    continue

                lineas = texto.split("\n")

                titulo = None
                precio = None
                kilometraje = None

                for l in lineas:
                    if re.search(r"\b(19[8-9][0-9]|20[0-2][0-9])\b", l):
                        titulo = l
                        break

                for l in lineas:
                    if "$" in l:
                        precio = limpiar_numero(l)
                        break

                for l in lineas:
                    if "km" in l.lower():
                        kilometraje = limpiar_numero(l)
                        break

                if not titulo:
                    continue

                marca, modelo = separar_marca_modelo(titulo)
                year = extraer_year(titulo)
                combustible = normalizar_combustible(texto)
                ciudad = extraer_ciudad(texto) or "santiago"

                try:
                    link = bloque.find_element(By.TAG_NAME, "a").get_attribute("href")
                except:
                    link = None

                if not link:
                    link = f"{url}#auto-{marca}-{modelo}-{year}-{precio}"

                if link in links_vistos:
                    continue

                links_vistos.add(link)

                auto = {
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
                    auto["combustible"],
                    auto["precio"]
                ]):
                    autos_extraidos.append(auto)

            except:
                continue

        if len(autos_extraidos) >= max_autos:
            break

    driver.quit()

    print("\n📊 RESULTADO FINAL")
    print(f"🚗 Autos extraídos: {len(autos_extraidos)}")

    return autos_extraidos


# =========================
# EJECUCIÓN LOCAL
# =========================
if __name__ == "__main__":
    datos = ejecutar_extraccion(max_autos=10)
    print("Total:", len(datos))