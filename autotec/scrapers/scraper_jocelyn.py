import os
import re
import time
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# =========================
# LIMPIEZA
# =========================
os.system("pkill -9 chrome")
os.system("pkill -9 chromedriver")
print("Limpieza lista.")

# =========================
# CONFIGURACIÓN
# =========================
NOMBRE_GRUPO = "AutoTec"
USUARIO = "jocelyn"
MAX_AUTOS = 500

urls_marcas = [
    "https://autos.cari.cl/autos/hyundai",
    "https://autos.cari.cl/autos/chevrolet",
    "https://autos.cari.cl/autos/toyota",
    "https://autos.cari.cl/autos/kia",
    "https://autos.cari.cl/autos/nissan",
    "https://autos.cari.cl/autos/mazda",
    "https://autos.cari.cl/autos/suzuki",
    "https://autos.cari.cl/autos/ford",
    "https://autos.cari.cl/autos/peugeot",
    "https://autos.cari.cl/autos/volkswagen",
    "https://autos.cari.cl/autos/subaru",
    "https://autos.cari.cl/autos/mitsubishi",
    "https://autos.cari.cl/autos/renault",
    "https://autos.cari.cl/autos/citroen",
    "https://autos.cari.cl/autos/chery",
    "https://autos.cari.cl/autos/jac",
    "https://autos.cari.cl/autos/mg",
    "https://autos.cari.cl/autos/fiat",
    "https://autos.cari.cl/autos/bmw",
    "https://autos.cari.cl/autos/mercedes-benz",
    "https://autos.cari.cl/autos/audi",
    "https://autos.cari.cl/autos/jeep",
    "https://autos.cari.cl/autos/great-wall",
    "https://autos.cari.cl/autos/changan",
    "https://autos.cari.cl/autos/ssangyong"
]

marcas_validas = [
    "hyundai", "chevrolet", "toyota", "kia", "nissan",
    "mazda", "suzuki", "ford", "peugeot", "volkswagen",
    "subaru", "mitsubishi", "renault", "citroen", "chery",
    "jac", "mg", "fiat", "bmw", "mercedes-benz", "mercedes",
    "audi", "jeep", "great-wall", "great wall", "changan",
    "ssangyong"
]

datos_finales = []
links_vistos = set()

# =========================
# SELENIUM
# =========================
options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--headless=new")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(options=options)

# =========================
# FUNCIONES
# =========================
def limpiar_precio(texto):
    if not texto:
        return 0.0
    limpio = re.sub(r"[^\d]", "", str(texto))
    return float(limpio) if limpio else 0.0


def extraer_precio(texto):
    match = re.search(r"\$\s?[\d\.]+", texto)
    return limpiar_precio(match.group(0)) if match else 0.0


def extraer_anio(texto):
    patrones = [
        r"Año\s*[:\-]?\s*(19\d{2}|20\d{2})",
        r"Modelo\s*[:\-]?\s*(19\d{2}|20\d{2})",
        r"\b(19\d{2}|20\d{2})\b"
    ]

    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            return int(match.group(1))

    return None


def extraer_kilometraje(texto):
    patrones = [
        r"Kilometraje\s*[:\-]?\s*(\d[\d\.\,]*)",
        r"(\d[\d\.\,]*)\s*(km|kms|kilómetros|kilometros)"
    ]

    for patron in patrones:
        match = re.search(patron, texto, re.IGNORECASE)
        if match:
            limpio = re.sub(r"[^\d]", "", match.group(1))
            return int(limpio) if limpio else None

    return None


def extraer_combustible(texto):
    t = texto.lower()

    if "gasolina" in t or "bencina" in t:
        return "Gasolina"
    if "diesel" in t or "diésel" in t:
        return "Diesel"
    if "híbrido" in t or "hibrido" in t:
        return "Híbrido"
    if "eléctrico" in t or "electrico" in t:
        return "Eléctrico"

    return None


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
            return ciudad

    return None


def normalizar_marca(marca_url):
    marca_url = marca_url.replace("-", " ")

    if marca_url == "mercedes benz":
        return "Mercedes-Benz"
    if marca_url == "great wall":
        return "Great Wall"

    return marca_url.title()


def extraer_nombre_auto(texto, marca_url):
    lineas = [x.strip() for x in texto.split("\n") if x.strip()]
    marca_limpia = marca_url.replace("-", " ").lower()

    for linea in lineas:
        linea_lower = linea.lower()

        if marca_limpia in linea_lower or marca_url.lower() in linea_lower:
            if "$" not in linea and "año" not in linea_lower and "kilometraje" not in linea_lower:
                return linea

    return None


def separar_marca_modelo(nombre, marca_url):
    marca_base = normalizar_marca(marca_url)

    if not nombre:
        return marca_base, "No disponible"

    nombre_limpio = nombre.strip()
    partes = nombre_limpio.split()
    marca_url_limpia = marca_url.replace("-", " ").lower()

    if nombre_limpio.lower().startswith(marca_url_limpia):
        modelo = nombre_limpio[len(marca_url_limpia):].strip()
        return marca_base, modelo if modelo else "No disponible"

    if len(partes) == 1:
        return marca_base, "No disponible"

    marca = partes[0]
    modelo = " ".join(partes[1:])

    return marca, modelo


# =========================
# SCRAPER 1: OBTENER LINKS
# =========================
def obtener_links_autos():
    links_autos = []

    for url_marca in urls_marcas:
        if len(links_autos) >= MAX_AUTOS:
            break

        marca_url = url_marca.rstrip("/").split("/")[-1]

        print(f"\nBuscando links en marca: {marca_url}")
        print(url_marca)

        try:
            driver.get(url_marca)
            time.sleep(6)

            enlaces = driver.find_elements(By.TAG_NAME, "a")
            encontrados_marca = 0

            for enlace in enlaces:
                href = enlace.get_attribute("href")

                if not href:
                    continue

                if href in links_vistos:
                    continue

                if "autos.cari.cl" not in href:
                    continue

                if f"/autos/{marca_url}" in href:
                    continue

                if "/autos/" in href or "/auto/" in href:
                    links_vistos.add(href)
                    links_autos.append(href)
                    encontrados_marca += 1

                if len(links_autos) >= MAX_AUTOS:
                    break

            print("Links encontrados en marca:", encontrados_marca)
            print("Total links acumulados:", len(links_autos))

        except Exception as e:
            print("Error buscando links en marca:", marca_url, e)
            continue

    return links_autos


# =========================
# SCRAPER 2: EXTRAER DETALLE
# =========================
def extraer_detalle_auto(url_auto):
    try:
        driver.get(url_auto)
        time.sleep(4)

        texto = driver.find_element(By.TAG_NAME, "body").text

        marca_url = None

        for marca in marcas_validas:
            marca_busqueda = marca.replace(" ", "-")
            if marca in url_auto.lower() or marca_busqueda in url_auto.lower():
                marca_url = marca
                break

        if not marca_url:
            marca_url = "no-disponible"

        nombre = extraer_nombre_auto(texto, marca_url)
        marca, modelo = separar_marca_modelo(nombre, marca_url)

        precio = extraer_precio(texto)
        year = extraer_anio(texto)
        kilometraje = extraer_kilometraje(texto)
        combustible = extraer_combustible(texto)
        ciudad = extraer_ciudad(texto)

        # Filtro menos estricto para probar guardado
        # Solo exige precio y año, los otros datos quedan como "No disponible" si no aparecen.
        if precio == 0 or not year:
            return None

        registro = {
            "marca": marca,
            "modelo": modelo,
            "year": year,
            "kilometraje": kilometraje if kilometraje else "No disponible",
            "combustible": combustible if combustible else "No disponible",
            "ciudad": ciudad if ciudad else "No disponible",
            "url": url_auto,
            "precio": precio,
            "usuario": USUARIO,
            "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
            "grupo": NOMBRE_GRUPO,
            "fuente": "autos.cari.cl"
        }

        return registro

    except Exception as e:
        print("Error en detalle:", url_auto, e)
        return None

# =========================
# VERIFICACIÓN FINAL
# =========================
print("\nTotal capturado en esta ejecución:", len(datos_finales))

if datos_finales:
    print("\nPrimer registro capturado:")
    print(datos_finales[0])

# =========================
# EXTRAER
# =========================
def ejecutar_extraccion(max_autos=5):
    global MAX_AUTOS, datos_finales, links_vistos

    MAX_AUTOS = max_autos
    datos_finales = []
    links_vistos = set()

    print("\nIniciando extracción de links...")
    links_autos = obtener_links_autos()

    print("\nTotal de links obtenidos:", len(links_autos))
    print("\nIniciando extracción de detalles...")

    for i, link in enumerate(links_autos, start=1):
        if len(datos_finales) >= MAX_AUTOS:
            break

        registro = extraer_detalle_auto(link)

        if registro:
            datos_finales.append(registro)
            print(f"Capturado {len(datos_finales)}/{MAX_AUTOS} | Link revisado {i}/{len(links_autos)}")
        else:
            print(f"Incompleto | Link revisado {i}/{len(links_autos)}")

    print("\nExtracción terminada.")
    print("Total autos capturados:", len(datos_finales))

    return datos_finales