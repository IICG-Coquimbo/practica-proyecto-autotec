import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# =========================
# LIMPIEZA
# =========================
os.system("pkill -9 chrome")
os.system("pkill -9 chromedriver")

# =========================
# CONFIGURACIÓN
# =========================
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
    "https://autos.cari.cl/autos/mitsubishi",
    "https://autos.cari.cl/autos/subaru",
    "https://autos.cari.cl/autos/honda",
    "https://autos.cari.cl/autos/renault",
    "https://autos.cari.cl/autos/citroen",
    "https://autos.cari.cl/autos/fiat",
    "https://autos.cari.cl/autos/jeep",
    "https://autos.cari.cl/autos/bmw",
    "https://autos.cari.cl/autos/audi",
    "https://autos.cari.cl/autos/mg"
]

marcas_validas = [url.split("/")[-1] for url in urls_marcas]

# =========================
# VARIABLES
# =========================
autos_vistos = set()
total_autos_validos = 0

# =========================
# SELENIUM
# =========================
options = Options()
options.binary_location = "/usr/bin/google-chrome"
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
)

driver = webdriver.Chrome(options=options)

# =========================
# FUNCIONES
# =========================
def limpiar_precio(texto):
    limpio = re.sub(r"[^\d]", "", texto)
    return float(limpio) if limpio else 0

def extraer_precio(texto):
    match = re.search(r"\$\s?[\d\.]+", texto)
    return limpiar_precio(match.group(0)) if match else 0

def extraer_anio(texto):
    match = re.search(r"\b(19\d{2}|20\d{2})\b", texto)
    return int(match.group(0)) if match else None

def extraer_nombre(lineas):
    for linea in lineas:
        if any(m in linea.lower() for m in marcas_validas):
            if "$" not in linea.lower() and "año" not in linea.lower():
                return linea.strip()
    return None

# =========================
# SCRAPING
# =========================
try:
    for url in urls_marcas:

        if total_autos_validos >= MAX_AUTOS:
            break

        marca_actual = url.split("/")[-1]
        autos_validos_por_marca = 0

        print(f"\nProcesando marca: {marca_actual}")

        try:
            driver.get(url)
        except:
            print("Error al cargar la página")
            continue

        time.sleep(8)

        # scroll para cargar más autos
        for _ in range(5):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        elementos_detectados = driver.find_elements(
            By.CSS_SELECTOR,
            "article, li[itemtype='http://schema.org/Product'], div[class*='item']"
        )

        print("Elementos detectados (sin filtrar):", len(elementos_detectados))

        for elemento in elementos_detectados:

            if total_autos_validos >= MAX_AUTOS:
                break

            texto = elemento.text.strip()

            if not texto or "$" not in texto:
                continue

            lineas = [x.strip() for x in texto.split("\n") if x.strip()]

            nombre = extraer_nombre(lineas)
            if not nombre:
                continue

            precio = extraer_precio(texto)
            if precio == 0:
                continue

            anio = extraer_anio(texto)

            clave_unica = f"{nombre}-{precio}-{anio}"

            if clave_unica in autos_vistos:
                continue

            autos_vistos.add(clave_unica)

            autos_validos_por_marca += 1
            total_autos_validos += 1

        print("Autos válidos en esta marca:", autos_validos_por_marca)
        print("Total autos válidos acumulados:", total_autos_validos)

    print("\n===== RESULTADO FINAL =====")
    print("Total autos extraídos:", total_autos_validos)

finally:
    driver.quit()