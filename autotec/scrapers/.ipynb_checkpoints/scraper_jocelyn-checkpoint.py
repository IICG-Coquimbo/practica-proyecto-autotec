import os
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================
# CONFIGURACIÓN PROYECTO
# =========================
NOMBRE_GRUPO = "AutoTec"
USUARIO = "jocelyn"

# URLs que confirmaste que funcionan
URLS_MARCAS = [
    "https://autos.cari.cl/autos/hyundai", "https://autos.cari.cl/autos/chevrolet",
    "https://autos.cari.cl/autos/toyota", "https://autos.cari.cl/autos/kia",
    "https://autos.cari.cl/autos/nissan", "https://autos.cari.cl/autos/mazda",
    "https://autos.cari.cl/autos/suzuki", "https://autos.cari.cl/autos/ford"
]

MARCAS_VALIDAS = [
    "hyundai", "chevrolet", "toyota", "kia", "nissan", "mazda", "suzuki", "ford"
]

def limpiar_sistema():
    """Mata procesos huérfanos para evitar el 'Server Connection Error'"""
    os.system("pkill -9 chrome")
    os.system("pkill -9 chromedriver")
    print("🧹 Memoria del sistema liberada.")

def extraer_precio(texto):
    match = re.search(r"\$\s?[\d\.]+", texto)
    if match:
        limpio = re.sub(r"[^\d]", "", match.group(0))
        return float(limpio) if limpio else 0.0
    return 0.0

def extraer_anio(texto):
    match = re.search(r"\b(19\d{2}|20\d{2})\b", texto)
    return int(match.group(1)) if match else None

def ejecutar_extraccion(max_autos=50):
    # 1. Limpieza preventiva
    limpiar_sistema()
    
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=options)
    links_vistos = set()
    datos_finales = []

    try:
        print(f"🚀 [Jocelyn] Iniciando Cari.cl...")

        # FASE 1: Obtener Links con Scroll
        links_autos = []
        for url_marca in URLS_MARCAS:
            if len(links_autos) >= max_autos: break
            
            try:
                driver.get(url_marca)
                time.sleep(5) # Espera carga inicial
                
                # --- TRUCO DE SCROLL: Baja 3 veces para cargar autos ocultos ---
                for _ in range(3):
                    driver.execute_script("window.scrollBy(0, 800);")
                    time.sleep(2)
                
                enlaces = driver.find_elements(By.TAG_NAME, "a")
                encontrados_esta_marca = 0
                
                for enlace in enlaces:
                    href = enlace.get_attribute("href")
                    if href and "/auto/" in href and href not in links_vistos:
                        # Filtro para evitar links de categorías
                        if not any(x in href for x in ["/autos/", "?page="]):
                            links_vistos.add(href)
                            links_autos.append(href)
                            encontrados_esta_marca += 1
                            if len(links_autos) >= max_autos: break
                
                print(f"  📂 {url_marca.split('/')[-1].upper()}: +{encontrados_esta_marca} links.")
            except:
                continue

        # FASE 2: Extraer detalles de cada link
        if not links_autos:
            print("⚠️ No se encontraron links. Revisa la conexión o el bloqueo del sitio.")
            return []

        print(f"🔗 Procesando {len(links_autos)} vehículos...")
        for i, link in enumerate(links_autos, start=1):
            try:
                driver.get(link)
                time.sleep(3)
                cuerpo = driver.find_element(By.TAG_NAME, "body").text
                
                precio = extraer_precio(cuerpo)
                year = extraer_anio(cuerpo)
                
                if precio > 0 and year:
                    # Sacamos marca/modelo del slug del link
                    slug = link.split("/")[-2].replace("-", " ").title()
                    partes = slug.split()
                    
                    registro = {
                        "marca": partes[0] if partes else "N/A",
                        "modelo": " ".join(partes[1:]) if len(partes) > 1 else "N/A",
                        "year": year,
                        "kilometraje": "No disponible", # Se puede pulir con regex
                        "combustible": "No disponible",
                        "ciudad": "Chile",
                        "url": link,
                        "precio": int(precio),
                        "usuario": USUARIO,
                        "fecha_captura": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "grupo": NOMBRE_GRUPO,
                        "fuente": "autos.cari.cl"
                    }
                    datos_finales.append(registro)
                    if i % 5 == 0: print(f"  📝 {i}/{len(links_autos)} completados...")
            except:
                continue

    finally:
        driver.quit()
        print(f"🔒 Jocelyn finalizado. Total capturados: {len(datos_finales)}")

    return datos_finales